# Seed Reference Verification (S01–S18)

Run date: 2026-11-23. Method: Crossref REST API (OA-02).
- When the seed had a candidate DOI, it was resolved with `works/{doi}`.
- Otherwise `works?query.bibliographic=<title>&rows=3` was used.
- A seed counts as verified (Y) when the normalised title similarity is ≥ 0.85 for a DOI lookup, or ≥ 0.90 with a year within ±1 for a title search.
- Raw results are in `search_runs/seed_crossref.json`. The input titles and DOIs are in `search_runs/seeds_input.json`.

> `seed_references.md` was **not modified**. The corrections below are proposals for the research-lead and student. Once accepted, update the seed file and set the status from VERIFY to VERIFIED.

## Verification table

| # | Seed (short) | Candidate DOI in seed file | Crossref result | Title match | Verified | Corrections / notes |
|---|---|---|---|---|---|---|
| S01 | Page et al. (2021) PRISMA 2020, *BMJ* | 10.1136/bmj.n71 | 10.1136/bmj.n71 | 1.00 | **Y** | Crossref gives article number n71 and no volume field. Keep *BMJ, 372*, n71 from the publisher page. |
| S02 | Kitchenham & Charters (2007) EBSE technical report | n/a (report) | Title search returned **a different work**: Budgen & Brereton (2006), "Performing systematic literature reviews in software engineering", ICSE '06, 10.1145/1134285.1134500 | 1.00 (substring match: false positive) | **N** | The technical report has no DOI and is not in Crossref. Cite it as a report and verify on the Keele/Durham repository. Do **not** use the Budgen & Brereton DOI. |
| S03 | Webster & Watson (2002), *MIS Quarterly* | (blank) | 10.2307/4132319 | 1.00 | **Y** | DOI found: **10.2307/4132319**. Vol. 26(2), pp. xiii–xxiii confirmed. |
| S04 | Wohlin (2014) snowballing, EASE | (blank) | 10.1145/2601248.2601268 | 1.00 | **Y** | DOI found: **10.1145/2601248.2601268**. Pages 1–10 (article 38 in ACM metadata, to be checked). |
| S05 | Hevner et al. (2004), *MIS Quarterly* | 10.2307/25148625 | 10.2307/25148625 | 1.00 | **Y** | Crossref gives pages **75–106** and the seed file says 75–105. Check against the JSTOR PDF. |
| S06 | Peffers et al. (2007), *JMIS* | 10.2753/MIS0742-1222240302 | 10.2753/mis0742-1222240302 | 1.00 | **Y** | Vol. 24(3), 45–77 confirmed. |
| S07 | Grieves & Vickers (2017), Springer chapter | (blank) | 10.1007/978-3-319-38756-7_4 | 1.00 | **Y** | DOI found: **10.1007/978-3-319-38756-7_4**, pp. 85–113. Crossref issued-date is **2016** (online), while the seed file says 2017 (print). APA 7 uses the copyright year of the book, so check the copyright page. |
| S08 | Sacks et al. (2020), *Data-Centric Engineering* | 10.1017/dce.2020.16 | 10.1017/dce.2020.16 | 1.00 | **Y** | Vol. 1, e14. Five authors confirmed (incl. Girolami). Retrieved in SLR (R0137). |
| S09 | Boje et al. (2020), *Automation in Construction* | 10.1016/j.autcon.2020.103179 | same | 1.00 | **Y** | Vol. 114, 103179. Retrieved in SLR (R0187). |
| S10 | Opoku et al. (2021), *J. Building Engineering* | 10.1016/j.jobe.2021.102726 | same | 1.00 | **Y** | Vol. 40, 102726. Retrieved in SLR (R0185). |
| S11 | Siebert & Teizer (2014), *Automation in Construction* | 10.1016/j.autcon.2014.01.004 | same | 1.00 | **Y** | Vol. 41, 1–14. Retrieved in SLR (R3119) via a title-only string. |
| S12 | Golparvar-Fard et al. (2009), *J. Computing in Civil Engineering* | (blank) | 10.1061/(ASCE)0887-3801(2009)23:6(391) | 1.00 | **Y** (JCCE paper) | DOI found. Vol. 23(6), 391–404 confirmed. The **alternative D4AR paper (ITcon 14, 2009) was not found in Crossref**, because ITcon does not register DOIs. Recommendation: cite the JCCE paper. It is pre-2010, so flag it SEMINAL. |
| S13 | Omar & Nehdi (2016), *Automation in Construction* | 10.1016/j.autcon.2016.06.016 | same | 1.00 | **Y** | Vol. 70, 143–155. Retrieved in SLR (R3376). |
| S14 | Akhavian & Behzadan (2015), *AEI* | 10.1016/j.aei.2015.03.001 | same | 1.00 | **Y** | Vol. 29(4), 867–877. Retrieved in SLR (R3262). |
| S15 | Teizer (2015), *AEI* | (blank) | 10.1016/j.aei.2015.03.006 | 1.00 | **Y** | DOI found: **10.1016/j.aei.2015.03.006**. Vol. 29(2), 225–238 confirmed. Retrieved in SLR (R3263). |
| S16 | Fleming & Koppelman (2010), *Earned value project management* (4th ed.), PMI | n/a (book) | No reliable match. The best candidate was an unrelated BSI document (similarity 0.69). | – | **N** | Book without a DOI in Crossref. Verify the edition and year against the PMI or library catalogue (ISBN). |
| S17 | Davis (1989), *MIS Quarterly* | 10.2307/249008 | same | 1.00 | **Y** | Vol. 13(3), 319–340 confirmed. |
| S18 | Venkatesh et al. (2003), *MIS Quarterly* | 10.2307/30036540 | same | 1.00 | **Y** | Vol. 27(3), 425–478 confirmed. |

## Summary

- **15 of 18 seeds verified** in Crossref: S01, S03–S15 and S17–S18.
  - S12 was verified for the JCCE version only.
  - The DOIs found by title search are S03, S04, S07, S12 and S15. Add them to `seed_references.md`.
- **3 seeds not verifiable in Crossref:**
  - S02 (technical report). The title search produced a false positive, which shows why substring matches need a human check.
  - S12-alternative D4AR (ITcon, no DOIs).
  - S16 (book).
  - These need catalogue or ISBN verification, not DOI verification.
- **Gold-set retrieval in the SLR:** 7 of 8 domain seeds (S08–S15) were retrieved by the OpenAlex strings (v1.1). S12 is pre-2010 and outside the date limit.
- **Proposed corrections:**
  - S05: pages, to be checked.
  - S07: year 2016 vs 2017, to be checked.
  - S12: choose the JCCE paper.
  - S02: no DOI.
- The **verified seeds** are written to `references.bib` with a `seed Sxx` note: the 7 domain seeds through the core set, plus S01, S03–S07, S12, S17 and S18.
- **Standards N01–N08 and practice sources P01–P02** are not bibliographic DOIs and were not checked in this run. They need verification of edition and version against ISO, IEC and IPLOCA catalogues.
