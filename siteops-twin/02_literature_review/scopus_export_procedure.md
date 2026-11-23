# Scopus Searches Run by the Student (D-072 amendment)

The searches are run **by the student** under their own POLIMI/Elsevier access. Credentials are never shared with an agent. The agent then does deduplication, screening support, the reference matrix and DOI verification on the exported files.

1. Log in to Scopus through the POLIMI library (institutional access).
2. In *Advanced document search*, paste each string from `search_strings.md` (CORE-01, then C1–C9) **exactly as written**. Apply the limits in §1 (2010–2026; article, conference paper, review; English or Italian).
3. Record the hit count and the date in the search log (`search_strings.md` §6).
4. Select all results, then **Export → CSV** with *Citation information*, *Bibliographical information*, *Abstract & keywords* and *Include references* (optional). Keep the file name `SCOPUS_<string-id>_<yyyymmdd>.csv`.
5. Put the files in `02_literature_review/exports/` (or send them in the chat). Do not include anything that identifies your account.
6. The literature-reviewer agent merges them with the OpenAlex/Crossref results, deduplicates by DOI and title, and fills `screening_log_template.csv` for stage 1.
