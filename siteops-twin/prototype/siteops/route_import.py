"""Import a real project route from a Google My Maps KML export (kept PRIVATE, git-ignored).

    python -m siteops.route_import <export.kml> [--name REGEX] [--title "..."]
        -> ../data/private/route.json   (lon/lat polyline + chainage)

Line segments are chained by nearest endpoints into one alignment. The synthetic demo chainage
(0..KP_END_M) is then positioned proportionally along the real route for display. The data stay synthetic;
only the map geometry is real. Points (stations, crossings) are kept as map labels.
"""
from __future__ import annotations

import json
import math
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

PRIVATE = Path(__file__).resolve().parent.parent.parent / "data" / "private"
NS = {"k": "http://www.opengis.net/kml/2.2"}


def hav(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


def length(pts):
    return sum(hav(a, b) for a, b in zip(pts, pts[1:]))


def parse(path: Path):
    data = path.read_bytes()
    if data[:2] == b"PK":  # KMZ
        with zipfile.ZipFile(path) as z:
            data = z.read(next(n for n in z.namelist() if n.endswith(".kml")))
    root = ET.fromstring(data)
    lines, points = [], []
    for pm in root.iter("{http://www.opengis.net/kml/2.2}Placemark"):
        name = (pm.findtext("k:name", default="", namespaces=NS) or "").strip()
        for ls in pm.iter("{http://www.opengis.net/kml/2.2}LineString"):
            txt = ls.findtext("k:coordinates", default="", namespaces=NS)
            pts = [tuple(map(float, c.split(",")[:2])) for c in txt.split() if c.count(",") >= 1]
            if len(pts) >= 2:
                lines.append({"name": name, "pts": pts})
        for pt in pm.iter("{http://www.opengis.net/kml/2.2}Point"):
            c = pt.findtext("k:coordinates", default="", namespaces=NS).strip().split(",")
            if len(c) >= 2:
                points.append({"name": name, "lon": float(c[0]), "lat": float(c[1])})
    return lines, points


def chain(lines, tol_m=300.0):
    """Greedy chaining of segments into one alignment, starting from the longest."""
    segs = sorted((l["pts"] for l in lines), key=length, reverse=True)
    path = list(segs.pop(0))
    changed = True
    while segs and changed:
        changed = False
        for i, s in enumerate(segs):
            for cand, at_end in ((s, True), (s[::-1], True), (s, False), (s[::-1], False)):
                if at_end and hav(path[-1], cand[0]) <= tol_m:
                    path += list(cand[1:]); segs.pop(i); changed = True; break
                if not at_end and hav(cand[-1], path[0]) <= tol_m:
                    path = list(cand[:-1]) + path; segs.pop(i); changed = True; break
            if changed:
                break
    return path, len(segs)


def build(kml: Path, name_regex: str | None = None, title: str | None = None, out: Path = PRIVATE / "route.json"):
    lines, points = parse(kml)
    if name_regex:
        lines = [l for l in lines if re.search(name_regex, l["name"], re.I)]
    if not lines:
        raise SystemExit("No LineString found in the KML (check --name filter).")
    path, unused = chain(lines)
    kp, acc = [0.0], 0.0
    for a, b in zip(path, path[1:]):
        acc += hav(a, b)
        kp.append(round(acc, 2))
    out.parent.mkdir(parents=True, exist_ok=True)
    rec = {"title": title or "Map: real project route (synthetic data positioned along it)", "length_m": round(acc, 1),
           "points": [[round(x, 7), round(y, 7)] for x, y in path], "kp": kp, "pois": points,
           "segments_in_kml": len(lines), "segments_not_chained": unused, "source": kml.name}
    out.write_text(json.dumps(rec), encoding="utf-8")
    print(f"route: {len(path)} vertices, {acc / 1000:.2f} km, {len(lines)} line(s), {unused} not chained, {len(points)} points -> {out}")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); raise SystemExit(1)
    nm = args[args.index("--name") + 1] if "--name" in args else None
    tt = args[args.index("--title") + 1] if "--title" in args else None
    build(Path(args[0]), nm, tt)
