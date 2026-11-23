#!/usr/bin/env python3
"""Reproducible OpenAlex search runner for the SiteOps Twin SLR (Amendment A1, D-072).

Usage:  python3 run_openalex.py           (from this directory)
Writes: <QUERY_ID>.json (trimmed records) per query, and appends rows to ../search_log.csv.
No personal data is sent; a generic User-Agent is used.
"""
import csv, json, os, time, urllib.parse, urllib.request

UA = "SiteOpsTwin-SLR/0.1 (research; mailto omitted)"
BASE = "https://api.openalex.org/works"
RUN_DATE = "2026-11-23"
LIMITS = "from_publication_date:2010-01-01,type:article|review|book-chapter|conference-paper,language:en"
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "..", "search_log.csv")
PER_QUERY = 200

# OpenAlex boolean translation of search_strings.md (Scopus truncation '*' is not supported by
# OpenAlex; plural/variant forms are listed explicitly and OpenAlex stemming covers the rest).
QUERIES = {
 "CORE-01": '(pipeline OR pipelines OR "linear infrastructure" OR "linear project" OR "right-of-way" OR "right of way" OR corridor OR "oil and gas" OR highway OR railway OR road) AND ("digital twin" OR UAV OR UAS OR drone OR "unmanned aerial" OR photogrammetry OR orthophoto OR "point cloud") AND ("progress monitoring" OR "progress measurement" OR "progress tracking" OR "quantity takeoff" OR "quantity take-off" OR "earthwork volume" OR "volume calculation" OR "progress payment" OR invoice OR subcontractor OR "quantity surveying" OR "as-built") AND (construction OR contractor OR "construction site")',
 "C1": '("digital twin" OR "cyber-physical system") AND (construction OR "oil and gas" OR pipeline OR pipelines OR "linear infrastructure") AND (monitoring OR progress OR "site operation" OR production OR management)',
 "C2": '(UAV OR UAS OR drone OR "unmanned aerial") AND (photogrammetry OR "structure from motion" OR orthophoto OR orthomosaic OR DSM OR DEM OR DTM OR "point cloud") AND (earthwork OR volume OR stockpile OR excavation OR "construction site") AND (accuracy OR uncertainty OR "ground control point" OR GCP OR RTK OR PPK OR validation)',
 "C3": '(BIM OR "building information modeling" OR "building information modelling" OR "infrastructure information model") AND (GIS OR "geographic information" OR geospatial) AND ("linear infrastructure" OR pipeline OR highway OR road OR railway OR corridor OR "linear referencing" OR chainage OR stationing OR alignment)',
 "C4": '(RFID OR BLE OR "bluetooth low energy" OR UWB OR "ultra-wideband" OR GNSS OR GPS OR telematics OR IoT OR "internet of things" OR wearable OR "computer vision" OR "activity recognition") AND (worker OR workers OR labor OR labour OR crew OR equipment OR machinery OR "heavy equipment" OR fleet) AND (construction OR "construction site" OR "construction project") AND (tracking OR localization OR localisation OR monitoring OR productivity OR "idle time")',
 "C4-ETH": '(privacy OR ethics OR ethical OR surveillance OR consent OR GDPR) AND (tracking OR wearable OR localization OR "location data" OR monitoring) AND (worker OR workers OR employee OR labour OR labor) AND (construction OR "construction site")',
 "C5": '("productivity monitoring" OR "productivity measurement" OR "labor productivity" OR "labour productivity" OR "equipment productivity" OR "earned value" OR "schedule performance") AND (construction OR contractor OR "construction project") AND (automated OR automatic OR automation OR "real-time" OR "real time" OR sensor OR sensors OR "data-driven" OR dashboard OR digital)',
 "C6": '("progress payment" OR "interim payment" OR "payment application" OR "payment certificate" OR "payment certification" OR invoice OR invoicing OR "quantity takeoff" OR "quantity take-off" OR "quantity surveying" OR "measurement of work" OR "progress measurement" OR "as-built quantities") AND (subcontractor OR subcontractors OR contractor OR "construction project" OR construction) AND (automated OR automation OR verification OR digital OR dispute OR disputes OR claim OR claims OR "payment delay" OR blockchain OR "smart contract")',
 "C7": '(IFC OR "industry foundation classes" OR LandXML OR "ISO 19650" OR "OPC UA" OR OGC OR CityGML OR "3D Tiles" OR PODS OR "pipeline open data standard" OR "ISO 15143" OR "linked data" OR ontology OR "application programming interface") AND (interoperability OR integration OR "data exchange" OR schema) AND (construction OR infrastructure OR pipeline OR "digital twin")',
 "C8": '("data quality" OR "measurement uncertainty" OR "volume uncertainty" OR "data validation" OR provenance OR "audit trail" OR auditability OR traceability OR "data integrity") AND (construction OR "digital twin" OR "progress monitoring")',
 "C9": '("technology adoption" OR "technology acceptance" OR TAM OR UTAUT OR "diffusion of innovation" OR "resistance to change" OR "change management" OR "digital transformation") AND (construction OR contractor OR "construction industry" OR "construction site") AND (digital OR BIM OR "digital twin" OR drone OR UAV OR IoT OR wearable OR tracking OR "mobile application")',
 # Supplementary open-source equivalents of GS-01..GS-07 (pipeline / commercial focus)
 "SUP-PIPE": '(pipeline OR pipelines) AND (construction) AND ("right-of-way" OR "right of way" OR spread OR trench OR trenching OR "as-built" OR "progress" OR UAV OR drone OR "digital twin" OR GIS OR productivity) NOT (leak OR "in-line inspection" OR corrosion OR "machine learning pipeline")',
 "SUP-PAY": '("subcontractor payment" OR "interim payment" OR "progress payment" OR "payment delay" OR "payment certification" OR "construction payment") AND (construction) AND (dispute OR disputes OR automation OR blockchain OR "smart contract" OR verification OR digital)',
}

# Title-only supplementary strings (remedy for missing publisher abstracts in OpenAlex, e.g. many
# Elsevier records): run with filter title.search and ranked by citations (gold-set remedy).
TITLE_QUERIES = {
 "TTL-C1": '"digital twin" AND (construction OR pipeline OR pipelines OR infrastructure OR "oil and gas")',
 "TTL-C2": '(UAV OR UAS OR drone OR drones OR "unmanned aerial") AND (earthwork OR earthworks OR volume OR volumes OR stockpile OR construction OR surveying OR pipeline OR road OR highway)',
 "TTL-C4": '(tracking OR localization OR "activity recognition" OR telematics OR RFID OR GPS OR GNSS OR UWB OR "real-time location") AND (construction OR earthmoving OR "heavy equipment") AND (equipment OR workers OR worker OR resources OR labor OR machinery OR site OR sites)',
 "TTL-C6": '("progress monitoring" OR "progress tracking" OR "progress measurement" OR "progress estimation" OR "quantity takeoff" OR "quantity take-off" OR "progress payment" OR "interim payment" OR "payment" OR subcontractor OR subcontractors) AND (construction OR earthwork OR contractor OR infrastructure)',
}

FIELDS = "id,doi,title,display_name,publication_year,primary_location,type,cited_by_count,authorships,abstract_inverted_index,relevance_score"


def abstract(inv):
    if not inv:
        return ""
    pos = {}
    for w, idx in inv.items():
        for i in idx:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))[:1500]


def trim(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return {
        "id": w.get("id"),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower() or None,
        "title": w.get("title") or w.get("display_name"),
        "publication_year": w.get("publication_year"),
        "source": src.get("display_name"),
        "type": w.get("type"),
        "cited_by_count": w.get("cited_by_count"),
        "relevance_score": w.get("relevance_score"),
        "authors": [a.get("author", {}).get("display_name") for a in (w.get("authorships") or [])][:6],
        "n_authors": len(w.get("authorships") or []),
        "abstract": abstract(w.get("abstract_inverted_index")),
    }


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa
            time.sleep(2 + 3 * attempt)
            last = e
    raise last


def main(sort_key="relevance_score:desc", suffix="", n=PER_QUERY, only=None, queries=None, field="title_and_abstract.search"):
    queries = queries or QUERIES
    new_log = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as fh:
        wr = csv.writer(fh)
        if new_log:
            wr.writerow(["run_date", "database", "string_id", "string_version", "query_url",
                         "hits_raw", "hits_after_limits", "exported", "export_file", "notes"])
        for qid0, q in queries.items():
            if only and qid0 not in only:
                continue
            qid = qid0 + suffix
            raw_url = BASE + "?" + urllib.parse.urlencode({"filter": f"{field}:{q}", "per-page": 1})
            hits_raw = get(raw_url)["meta"]["count"]
            params = {"filter": f"{field}:{q},{LIMITS}", "sort": sort_key,
                      "per-page": n, "select": FIELDS}
            url = BASE + "?" + urllib.parse.urlencode(params)
            data = get(url)
            recs = [trim(w) for w in data["results"]]
            out = f"{qid}.json"
            with open(os.path.join(HERE, out), "w") as o:
                json.dump({"query_id": qid, "run_date": RUN_DATE, "query_url": url,
                           "hits_total": data["meta"]["count"], "retrieved": len(recs), "records": recs}, o, indent=1)
            wr.writerow([RUN_DATE, "OpenAlex", qid, "v1.1-OA", url, hits_raw, data["meta"]["count"], len(recs),
                         f"search_runs/{out}", f"{field} boolean; sort={sort_key}; top {n} retrieved"])
            print(qid, hits_raw, data["meta"]["count"], len(recs))
            time.sleep(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cited":
        # Second ranking pass (gold-set remedy, see prisma_flow.md): top-100 most-cited per string
        main(sort_key="cited_by_count:desc", suffix="-CIT", n=100,
             only=["CORE-01", "C1", "C2", "C3", "C4", "C4-ETH", "C5", "C6", "C7", "C8", "C9"])
    elif len(sys.argv) > 1 and sys.argv[1] == "title":
        main(sort_key="cited_by_count:desc", n=150, queries=TITLE_QUERIES, field="title.search")
    else:
        main()
