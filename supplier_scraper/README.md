# Supplier discovery scraper

Searches a B2B directory for a keyword, walks the result pages, opens every
company profile, and writes a clean vendor CSV for sourcing / long-listing.

```
supplier_scraper/
├── scraper.py            # the scraper (search → paginate → profile → CSV)
├── site_profiles.py      # per-directory selector profiles (europages, wlw, generic)
├── tools/mock_site.py    # local fixture directory used by the self test
├── run_fixture_test.sh   # end-to-end self test, writes vendors.sample.csv
├── requirements.txt
├── .env.example          # copy to .env and edit
└── vendors.sample.csv    # output of the self test (fixture data, NOT real vendors)
```

## Status of the live run — read this first

This project was built and tested inside a sandbox whose **egress policy blocks
every B2B directory host**. `europages.de`, `europages.it`, `europages.co.uk`,
`wlw.de`, `kompass.com`, `thomasnet.com`, `exportpages.de` and
`industrystock.com` all fail at the CONNECT tunnel with `403 Forbidden`; only
`pypi.org` is reachable. That is a network-policy decision on the host, not a
block by the directories, and routing around it is explicitly not allowed.

So **`vendors.csv` has not been produced from live directory data**, and no
substitute was invented — fabricated supplier rows are worse than none for a
sourcing exercise. What is proven instead is the whole pipeline, end to end,
against a local fixture directory that reproduces the awkward parts of a real
one (see *Self test* below). Run `python scraper.py` from a machine with normal
internet access and you get the real `vendors.csv`.

The live attempt is on record and fails cleanly rather than silently:

```
ERROR  robots.txt for https://europages.co.uk unreachable (... Tunnel connection
       failed: 403 Forbidden) - refusing to crawl this host
WARN   SKIP (robots.txt unreachable - host blocked by network policy, offline,
       or refusing our requests; failing closed): https://europages.co.uk/...
```

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium      # only needed for JS-rendered sites
cp .env.example .env                       # then edit KEYWORD / TARGET_DOMAIN / MAX_PAGES
```

## Run

```bash
python scraper.py                                        # uses .env
python scraper.py --keyword "Schweissdienstleistungen" --domain europages.de --max-pages 5
python scraper.py --keyword "servizi di saldatura" --domain europages.it --engine playwright
```

Every `.env` value has a matching CLI flag, and the flag wins.

### Fix the selectors first — `--inspect`

`site_profiles.py` ships **best-known** selectors for europages and wlw, not
selectors verified against their live DOM (they were unreachable here, above).
Directories also reshuffle their markup regularly. Before a real run:

```bash
python scraper.py --inspect --domain europages.de --keyword "Schweissdienstleistungen"
```

That fetches page 1 plus one profile and prints the repeated block structure,
the pagination candidates, how many cards the current profile matches, the
JSON-LD it can see, and the full row the current selectors produce. Correct the
lists in `site_profiles.py` from that output — usually a two-minute edit of
`result_card`, `profile_link` and `next_page`.

If the real search URL pattern differs, paste it straight from your browser:

```bash
python scraper.py --search-url-template "https://www.europages.de/unternehmen/{page}/{keyword}.html"
```

`{keyword}` and `{page}` are substituted; `{domain}` is available too.

## Output

`vendors.csv`, one row per unique vendor, columns exactly as specified:

| column | source |
|---|---|
| `company_name` | JSON-LD `name` → `h1` → result card title |
| `website_url` | outbound link that is not the directory or a social network |
| `contact_email` | `mailto:` → `itemprop=email` → e-mail regex over page text |
| `contact_phone` | `tel:` → `itemprop=telephone` → international phone regex |
| `address_line` | street line only (postcode/city/country split out) |
| `city`, `postal_code`, `country` | JSON-LD `PostalAddress` → microdata → address regex → TLD |
| `profile_url` | the directory profile URL |
| `categories_or_services` | category/keyword links, comma-separated |
| `certifications_or_standards` | regex for ISO/EN/IATF/API/ASME/AD 2000/PED/ATEX/SCC |
| `marketplace_id_or_internal_id` | `data-company-id` etc., else the URL slug |
| `last_scraped_at` | ISO-8601 UTC timestamp of the profile fetch |

Missing values are written as empty strings — never `null`, never `NaN`.

## How it behaves

- **robots.txt is enforced before every fetch**, with its `Crawl-delay` honoured
  on top of the configured delay. Disallowed URLs are skipped and logged, never
  fetched. If robots.txt cannot be read at all, the host is refused
  (fail-closed) rather than crawled on an unknown policy. `--ignore-robots`
  exists; using it on a site you do not own is your call and your liability.
- **Rate limited** to a random 1.5–2.5 s between requests (configurable).
- **Retries** 3× with 2/4/8 s backoff on HTTP errors and network failures, then
  logs the item as skipped and moves on.
- **Requests-first, browser-on-demand.** `--engine auto` fetches static HTML;
  if page 1 yields no result cards it transparently restarts on Playwright,
  which is what JS-rendered directories like wlw.de need.
- **Layered extraction.** Site-profile CSS selectors, then schema.org JSON-LD,
  then microdata, then `mailto:`/`tel:` links and text regexes. A stale
  selector degrades a row; it does not empty it.
- **Deduplicated** on directory host + normalised company name, keeping
  whichever duplicate carries more populated fields.
- **Logs** to stdout and `scrape.log`; every skipped item carries its reason.
- **No logins, no paywalls, no CAPTCHA handling** — publicly listed business
  contact data only, which is also all this stores.

## Self test

```bash
./run_fixture_test.sh
```

Starts `tools/mock_site.py` on 127.0.0.1, scrapes it, stops it. The fixture
deliberately includes a robots.txt `Disallow`, a profile that 404s, a `rel=next`
link that disappears on the last page (forcing URL construction), three markup
styles (JSON-LD / microdata / plain HTML), profiles missing e-mail, website or
certifications, and the same company listed twice under different URLs.

Verified result — 12 profile URLs found across 3 pages, 10 visited, 2 skipped
(1 robots-disallowed, 1 HTTP 404), 1 duplicate collapsed, **9 unique vendors**,
zero nulls:

```
company_name                     website_url                              contact_email                      country  certifications
Nordwerk Schweißtechnik GmbH     https://www.nordwerk-schweisstechnik.de  info@nordwerk-schweisstechnik.de   Germany  ISO 9001:2015, ISO 3834-2, EN 1090-2
Rheinstahl Montage AG            https://rheinstahl-montage.de            kontakt@rheinstahl-montage.de      Germany  ISO 9001, ISO 45001
Südmetall Werke KG               https://www.suedmetall-werke.de          (none published)                   Germany  (none listed)
Adria Saldature S.r.l.           (none published)                         commerciale@adriasaldature.it      Italy    ISO 9001:2015, ISO 3834-3
PipeTec Anlagenbau GmbH          https://pipetec-anlagenbau.de            sales@pipetec-anlagenbau.de        Germany  ISO 9001:2015, ISO 14001, AD 2000, PED, ASME VIII
...
```

The JS-rendered route (`/jssearch`) exercises the Playwright fallback: static
HTML yields 0 cards, the browser yields 4, pagination and robots enforcement
continue unchanged.

## Fields that are consistently thin, and why

These are properties of B2B directories, not gaps in the scraper. Plan your
sourcing workflow around them:

1. **`contact_email` — the weakest field, expect roughly half empty.**
   Europages, wlw and Kompass all monetise the lead: the profile shows a
   contact *form*, and the address is revealed only behind it. Where a real
   address does appear it is usually a generic `info@`/`vertrieb@` mailbox, not
   a named buyer contact. The scraper takes what is publicly rendered and does
   not fill the form.
2. **`website_url` — missing on free/basic listings.** Outbound links are a
   paid feature on most directories, and the JSON-LD `url` field frequently
   holds the *directory's own* profile URL, which is rejected as a false
   positive. Social links are excluded for the same reason.
3. **`certifications_or_standards` — present only when the vendor typed it in.**
   No directory has a structured certification field, so this is recovered from
   free text. It catches ISO/EN/IATF/API/ASME/AD 2000/PED/ATEX/SCC reliably but
   **cannot be trusted for prequalification** — it is a self-declared claim
   scraped from marketing copy, with no certificate number, scope or validity
   date. Treat it as a screening hint and always request the certificate.
4. **`postal_code` / `city`** are strong when the profile emits JSON-LD
   `PostalAddress` and weaker when the address is one free-text line — the
   regex handles German/Italian 5-digit, Polish `NN-NNN` and UK formats, but
   unusual layouts fall back to leaving the whole line in `address_line`.
5. **`marketplace_id_or_internal_id`** is a directory-internal id where one is
   exposed in the markup, otherwise the URL slug. It is stable enough to
   de-duplicate against on re-runs, but it is not a VAT number or D-U-N-S, so
   it is not an identifier for a vendor master record.

For an actual vendor master, this CSV is the **long list**: it gets you name,
location, scope and a route to contact. Company registration number, VAT ID,
turnover, headcount and genuine certification status are not on these profiles
and need a prequalification questionnaire or a registry/credit source.

## Legal and data-protection notes

- Publicly listed **business** contact data only; no personal data beyond what
  the company itself publishes as its business contact, and no attempt to
  enrich it with named individuals.
- robots.txt is enforced by default and requests are deliberately slow.
- Check the directory's own terms of use before a production run —
  `robots.txt` permission is not the same as contractual permission, and
  several B2B directories restrict systematic extraction in their T&Cs
  regardless of what robots.txt says.
