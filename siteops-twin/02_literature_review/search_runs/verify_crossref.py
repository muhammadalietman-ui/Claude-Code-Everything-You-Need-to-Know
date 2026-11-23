#!/usr/bin/env python3
"""DOI verification against Crossref (OA-02) for the core set and the seed references.

verified_doi = Y when Crossref resolves the DOI and the normalised title similarity with the
OpenAlex/seed title is >= 0.85 (difflib ratio) or one title contains the other.
Records without a DOI are searched with query.bibliographic (rows=3); a candidate is accepted
only with similarity >= 0.90 and |year difference| <= 1.
Output: crossref_verification.json, seed_crossref.json
"""
import json, os, re, time, difflib, urllib.parse, urllib.request

UA = "SiteOpsTwin-SLR/0.1 (research; mailto omitted)"
HERE = os.path.dirname(os.path.abspath(__file__))


def norm(t):
    t = re.sub(r"<[^>]+>", " ", (t or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    if a in b or b in a:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 + 2 * k)
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def meta(m):
    return {
        "cr_title": (m.get("title") or [""])[0],
        "cr_container": (m.get("container-title") or [""])[0] if m.get("container-title") else "",
        "cr_year": ((m.get("issued") or {}).get("date-parts") or [[None]])[0][0],
        "cr_volume": m.get("volume"), "cr_issue": m.get("issue"), "cr_page": m.get("page"),
        "cr_article_number": m.get("article-number"),
        "cr_type": m.get("type"), "cr_publisher": m.get("publisher"),
        "cr_authors": [{"given": a.get("given", ""), "family": a.get("family", a.get("name", ""))} for a in (m.get("author") or [])],
        "cr_doi": (m.get("DOI") or "").lower(),
    }


def verify(title, doi, year=None):
    out = {"query_title": title, "query_doi": doi}
    if doi:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        out["crossref_url"] = url
        r = get(url)
        if r and r.get("message"):
            m = meta(r["message"])
            s = sim(title, m["cr_title"])
            out.update(m, title_similarity=round(s, 3), verified_doi="Y" if s >= 0.85 else "N",
                       method="works/{doi}")
            if s < 0.85:
                out["note"] = "DOI resolves but title does not match"
            return out
        out["note"] = "DOI not found in Crossref"
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": title, "rows": 3})
    out["crossref_url"] = url
    r = get(url)
    best = None
    for it in ((r or {}).get("message") or {}).get("items", []):
        m = meta(it)
        s = sim(title, m["cr_title"])
        if best is None or s > best[0]:
            best = (s, m)
    if best and best[0] >= 0.90 and (year is None or best[1]["cr_year"] is None or abs(best[1]["cr_year"] - year) <= 1):
        out.update(best[1], title_similarity=round(best[0], 3), verified_doi="Y", method="query.bibliographic",
                   note=(out.get("note", "") + "; DOI found via title search").strip("; "))
    else:
        out.update(verified_doi="N", method="query.bibliographic",
                   best_candidate=(best[1]["cr_title"], best[1]["cr_doi"], round(best[0], 3)) if best else None,
                   note=(out.get("note", "") + "; no reliable Crossref match").strip("; "))
    return out


def main():
    recs = {r["record_id"]: r for r in json.load(open(os.path.join(HERE, "dedup.json")))["records"]}
    core = [l.split() for l in open(os.path.join(HERE, "core_set.txt")) if l.startswith("R")]
    res = {}
    for rid, _ in core:
        r = recs[rid]
        res[rid] = verify(r["title"], r["doi"], r["publication_year"])
        time.sleep(0.3)
    json.dump({"run_date": "2026-11-23", "results": res}, open(os.path.join(HERE, "crossref_verification.json"), "w"), indent=1)
    print("core verified:", sum(v["verified_doi"] == "Y" for v in res.values()), "/", len(res))
    seeds = json.load(open(os.path.join(HERE, "seeds_input.json")))
    sres = {}
    for s in seeds:
        sres[s["id"]] = verify(s["title"], s.get("doi"), s.get("year"))
        sres[s["id"]]["seed"] = s
        time.sleep(0.3)
    json.dump({"run_date": "2026-11-23", "results": sres}, open(os.path.join(HERE, "seed_crossref.json"), "w"), indent=1)
    for k, v in sres.items():
        print(k, v["verified_doi"], v.get("cr_doi"), v.get("title_similarity"), v.get("note", ""))


if __name__ == "__main__":
    main()
