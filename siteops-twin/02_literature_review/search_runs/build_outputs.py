#!/usr/bin/env python3
"""Builds screening_log.csv, reference_matrix.csv, references.bib and stats.json from the run files."""
import csv, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from coding import CODES  # noqa: E402

SCREENER = "AI-assisted (to be validated by student)"
# Documented manual overrides of the keyword rules (Stage 1), applied after rule screening.
OVERRIDES = {
    "R2072": ("Include", "", "manual override: O&G pipeline DT incl. engineering-construction stage (rule false exclusion)"),
    "R0147": ("Include", "", "manual override: O&G pipeline XR/DT review mentions construction challenges (rule false exclusion)"),
    "R3025": ("Include", "", "manual override: transport-infrastructure DT review covering design/construction (rule false exclusion)"),
}
DISAMBIG = {"R2225": "Hamledari & Fischer (2021a)", "R2226": "Hamledari & Fischer (2021b)", "R2104": "Khan et al. (2026a)", "R0017": "Khan et al. (2026b)"}
NAMECHECK = {"R0190", "R2072", "R2100", "R1889", "R0024"}
SEED_WRONG = {"S02": "Crossref title search returned Budgen & Brereton (2006) ICSE paper 'Performing systematic literature reviews in software engineering' (10.1145/1134285.1134500) - a different work; the Kitchenham & Charters (2007) EBSE technical report has no DOI"}


def initials(given):
    parts = re.split(r"[\s]+", (given or "").strip())
    out = []
    for p in parts:
        if not p:
            continue
        sub = [s for s in p.split("-") if s]
        out.append("-".join(s[0].upper() + "." for s in sub))
    return " ".join(out)


def apa_authors(auth):
    names = [f"{a['family']}, {initials(a['given'])}".strip().rstrip(",") if a.get("given") else a["family"] for a in auth if a.get("family")]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) <= 20:
        return ", ".join(names[:-1]) + ", & " + names[-1]
    return ", ".join(names[:19]) + ", ... " + names[-1]


def intext(auth, year):
    fam = [a["family"] for a in auth if a.get("family")]
    if not fam:
        return f"(n.a., {year})"
    if len(fam) == 1:
        return f"{fam[0]}, {year}"
    if len(fam) == 2:
        return f"{fam[0]} & {fam[1]}, {year}"
    return f"{fam[0]} et al., {year}"


def clean(t):
    t = re.sub(r"<[^>]+>", "", t or "")
    return t.replace("&amp;", "&").replace("\n", " ").strip()


def apa(v, fallback):
    au = apa_authors(v.get("cr_authors") or [])
    yr = v.get("cr_year") or fallback.get("publication_year")
    title = clean(v.get("cr_title") or fallback.get("title"))
    cont = clean(v.get("cr_container") or fallback.get("source") or "")
    s = f"{au} ({yr}). {title}."
    if cont:
        s += f" {cont}"
        if v.get("cr_volume"):
            s += f", {v['cr_volume']}"
            if v.get("cr_issue"):
                s += f"({v['cr_issue']})"
        if v.get("cr_page"):
            s += f", {v['cr_page']}"
        elif v.get("cr_article_number"):
            s += f", {v['cr_article_number']}"
        s += "."
    if v.get("cr_doi"):
        s += f" https://doi.org/{v['cr_doi']}"
    return s


def bibkey(v, used):
    fam = (v.get("cr_authors") or [{"family": "Anon"}])[0].get("family") or "Anon"
    fam = re.sub(r"[^A-Za-z]", "", fam.encode("ascii", "ignore").decode()) or "Anon"
    w = [x for x in re.findall(r"[A-Za-z]+", clean(v.get("cr_title"))) if x.lower() not in ("a", "an", "the", "of", "on", "for", "and", "in", "to", "towards", "toward")]
    k = f"{fam}{v.get('cr_year')}{(w[0] if w else 'x').capitalize()}"
    base, i = k, 1
    while k in used:
        k = base + "abcdefghij"[i]
        i += 1
    used.add(k)
    return k


def esc(t):
    return re.sub(r"(?<!\\)([&%#_])", r"\\\1", t or "")


def bibtex(v, key, note=None):
    typ = {"journal-article": "article", "proceedings-article": "inproceedings", "book-chapter": "incollection",
           "book": "book", "posted-content": "misc"}.get(v.get("cr_type"), "misc")
    auth = " and ".join(f"{a['family']}, {a['given']}".strip(", ") for a in (v.get("cr_authors") or []) if a.get("family"))
    f = {"author": auth, "title": "{" + esc(clean(v.get("cr_title"))) + "}", "year": str(v.get("cr_year") or ""), "doi": v.get("cr_doi")}
    cont = esc(clean(v.get("cr_container")))
    if typ == "article":
        f["journal"] = cont
    elif typ in ("inproceedings", "incollection"):
        f["booktitle"] = cont
    elif cont:
        f["howpublished"] = cont
    for a, b in (("volume", "cr_volume"), ("number", "cr_issue"), ("pages", "cr_page"), ("publisher", "cr_publisher")):
        if v.get(b):
            f[a] = str(v[b]).replace("-", "--") if a == "pages" else str(v[b])
    if not v.get("cr_page") and v.get("cr_article_number"):
        f["eid"] = str(v["cr_article_number"])
    if note:
        f["note"] = note
    body = ",\n".join(f"  {k} = {{{val}}}" if not val.startswith("{") else f"  {k} = {val}" for k, val in f.items() if val)
    return f"@{typ}{{{key},\n{body}\n}}\n"


def main():
    D = json.load(open(os.path.join(HERE, "dedup.json")))
    recs = D["records"]
    for rid, (dec, code, why) in OVERRIDES.items():
        r = next(x for x in recs if x["record_id"] == rid)
        r["override_from"] = f"{r['stage1_decision']} {r['stage1_reason_code']}".strip()
        r["stage1_decision"], r["stage1_reason_code"], r["stage1_reason"] = dec, code, why
    core = {l.split()[0]: l.split()[1] for l in open(os.path.join(HERE, "core_set.txt")) if l.startswith("R")}
    assert set(core) == set(CODES), set(core) ^ set(CODES)
    ver = json.load(open(os.path.join(HERE, "crossref_verification.json")))["results"]
    # Crossref author field of R0024 contains affiliation strings; author names taken from OpenAlex (documented).
    ver["R0024"]["cr_authors"] = [{"given": g, "family": f} for g, f in [("Aimi Nadira", "Mohd Safie"), ("Khairul Nizam", "Abdul Maulud"),
                                  ("Othman", "Jaafar"), ("Wan Shafrina", "Wan Mohd Jaafar"), ("Abdul Aziz", "Ab Rahman"), ("Faiz", "Arif")]]

    # ---- screening log
    with open(os.path.join(OUT, "screening_log.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["record_id", "source_db", "string_id", "authors", "year", "title", "doi", "stage1_decision", "stage1_reason_code",
                    "screener", "stage2_decision", "stage2_reason_code", "quality_score", "cluster", "notes"])
        for r in recs:
            rid = r["record_id"]
            cl = CODES[rid].split("|")[0] if rid in CODES else ";".join(r["clusters_kw"])
            notes = [r["stage1_reason"], f"abstract_source={r.get('abstract_source') or 'none'}", f"priority={r['priority']}"]
            if r.get("override_from"):
                notes.append(f"rule decision was '{r['override_from']}'")
            if rid in core:
                notes.append("CORE_SET=Y (abstract-level coded; see reference_matrix.csv)")
            s2 = "Pending (full text by student)" if r["stage1_decision"] in ("Include", "Unsure") else ""
            w.writerow([rid, "OpenAlex", ";".join(r["queries"]), "; ".join(a for a in r["authors"] if a) + ("; et al." if r["n_authors"] > 6 else ""),
                        r["publication_year"], r["title"], r["doi"] or "", r["stage1_decision"], r["stage1_reason_code"], SCREENER,
                        s2, "", "", cl, " | ".join(notes)])

    # ---- reference matrix
    tmpl = open(os.path.join(OUT, "reference_matrix_template.csv")).readline().strip().split(",")
    cmap = {"C1": "C1_digital_twin", "C2": "C2_uav_photogrammetry", "C3": "C3_bim_gis_linear", "C4": "C4_tracking", "C5": "C5_productivity_evm",
            "C6": "C6_progress_qty_payment", "C7": "C7_interoperability", "C8": "C8_data_quality", "C9": "C9_adoption"}
    rmap = {r["record_id"]: r for r in recs}
    seeds_in_core = {"R0137": "S08", "R0187": "S09", "R0185": "S10", "R3119": "S11", "R3376": "S13", "R3262": "S14", "R3263": "S15"}
    intexts, rows = {}, []
    order = sorted(core, key=lambda x: (core[x], x))
    for i, rid in enumerate(order, 1):
        r, v = rmap[rid], ver[rid]
        f = CODES[rid].split("|")
        assert len(f) == 19, (rid, len(f))
        cls = f[0].split(";")
        yr = v.get("cr_year") or r["publication_year"]
        if v["verified_doi"] == "Y":
            intexts[rid] = intext(v["cr_authors"], yr)
            cit = apa(v, r)
        else:
            cit = f"{'; '.join(a for a in r['authors'] if a)} ({r['publication_year']}). {r['title']}. {r['source'] or ''}. [DOI not verified via Crossref]"
        row = {"ref_id": f"REF-{i:03d}", "record_id": rid, "citation_apa": cit, "year": yr, "venue": clean(v.get("cr_container") or r["source"] or ""),
               "doi": v.get("cr_doi") or r["doi"] or "", "verified_doi": v["verified_doi"],
               "seminal": f"seed {seeds_in_core[rid]}" if rid in seeds_in_core else "N"}
        for c, col in cmap.items():
            row[col] = 1 if c in cls else 0
        keys = ["research_method", "sector_context", "project_type", "country_region", "data_sources", "technology", "quantity_or_metric_type",
                "validation_approach", "reported_accuracy_uncertainty", "key_findings", "limitations", "relevance_H1", "relevance_H2",
                "relevance_H3", "relevance_H4", "rq_mapping", "quality_band"]
        for k, val in zip(keys, f[1:18]):
            row[k] = val
        row["quality_band"] = f[17] + " (provisional, abstract-level)"
        row["extractor"] = "AI-assisted (to be validated by student)"
        row["notes"] = "; ".join(x for x in [f"primary cluster {core[rid]}", f"cited_by {r['cited_by_count']} (OpenAlex 2026-11-23)",
                                            f"abstract_source={r.get('abstract_source') or 'none'}", f[18]] if x)
        rows.append(row)
    with open(os.path.join(OUT, "reference_matrix.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=tmpl)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # ---- bibtex
    seeds = json.load(open(os.path.join(HERE, "seed_crossref.json")))["results"]
    used, bib, keys_by_rid = set(), [], {}
    bib.append("% references.bib - SiteOps Twin SLR (Phase 2, 2026-11-23)\n% Only entries whose DOI resolved in Crossref with a matching title (verified_doi = Y).\n"
               "% Generated from Crossref metadata by search_runs/build_outputs.py. Seeds marked with 'seed' in the note field.\n\n")
    done_dois = set()
    for rid in order:
        v = ver[rid]
        if v["verified_doi"] != "Y":
            continue
        k = bibkey(v, used)
        keys_by_rid[rid] = k
        note = (f"seed {seeds_in_core[rid]}; " if rid in seeds_in_core else "") + f"SLR core set {rid}"
        if rid in DISAMBIG:
            note += f"; cite as {DISAMBIG[rid].replace('&', '\\&')}"
        if rid in NAMECHECK:
            note += "; author name order in Crossref record to be checked"
        bib.append(bibtex(v, k, note))
        done_dois.add(v["cr_doi"])
    seed_keys = {}
    for sid, v in seeds.items():
        if v["verified_doi"] != "Y" or sid in SEED_WRONG or v.get("cr_doi") in done_dois:
            if v.get("cr_doi") in done_dois:
                seed_keys[sid] = "(in core set)"
            continue
        k = bibkey(v, used)
        seed_keys[sid] = k
        bib.append(bibtex(v, k, f"seed {sid} (methodological/seminal; not screened)"))
    open(os.path.join(OUT, "references.bib"), "w").write("\n".join(bib))

    # ---- stats
    inc = [r for r in recs if r["stage1_decision"] == "Include"]
    uns = [r for r in recs if r["stage1_decision"] == "Unsure"]
    exc = [r for r in recs if r["stage1_decision"] == "Exclude"]
    stats = {"identified": D["identified"], "unique": len(recs), "duplicates": D["identified"] - len(recs),
             "include": len(inc), "unsure": len(uns), "exclude": len(exc),
             "exclude_by_code": Counter(r["stage1_reason_code"] for r in exc), "core": len(core),
             "core_verified": sum(ver[x]["verified_doi"] == "Y" for x in core),
             "core_by_cluster": Counter(core.values()),
             "core_by_flag": Counter(c for x in core for c in CODES[x].split("|")[0].split(";")),
             "seed_status": {k: (("N (wrong match)" if k in SEED_WRONG else v["verified_doi"]), v.get("cr_doi")) for k, v in seeds.items()},
             "intext": intexts, "bibkeys": keys_by_rid, "seed_bibkeys": seed_keys}
    json.dump(stats, open(os.path.join(HERE, "stats.json"), "w"), indent=1, default=dict)
    print(json.dumps({k: v for k, v in stats.items() if k not in ("intext", "bibkeys")}, indent=1, default=dict))


if __name__ == "__main__":
    main()
