# Search Strategy and Search Strings

Owner: literature-reviewer. Version 0.1 (Phase 0). Status: **draft strings, not yet piloted**.

**[R]** In week 3, pilot each string, check that known key papers are retrieved (the "gold-set" test using `seed_references.md`), and then freeze the strings.

## 1. Common limits

| Limit | Scopus | Web of Science |
|---|---|---|
| Years | `PUBYEAR > 2009 AND PUBYEAR < 2027` | Publication Years 2010–2026 |
| Document type | `DOCTYPE(ar OR cp OR re)` | Article, Proceedings Paper, Review |
| Language | `LANGUAGE(english)` | Language: English |

- **Subject area (Scopus):** `LIMIT-TO(SUBJAREA,"ENGI") OR LIMIT-TO(SUBJAREA,"COMP") OR LIMIT-TO(SUBJAREA,"EART") OR LIMIT-TO(SUBJAREA,"BUSI") OR LIMIT-TO(SUBJAREA,"ENER") OR LIMIT-TO(SUBJAREA,"DECI")`. Apply it **after** recording the unlimited hit count.
- Record the hit count both before and after limits in the search log (§6).

## 2. Building blocks
| Block | Concept | Terms (Scopus syntax) |
|---|---|---|
| B-CON | Construction context | `"construction project*" OR "construction site*" OR "construction industry" OR "infrastructure project*" OR contractor*` |
| B-LIN | Linear / pipeline | `pipeline* OR "linear infrastructure" OR "linear project*" OR "right-of-way" OR "right of way" OR corridor* OR highway* OR railway* OR "transmission line*"` |
| B-OG | Oil & gas | `"oil and gas" OR "oil & gas" OR petroleum OR "gas pipeline*" OR "oil pipeline*" OR "midstream" OR EPC` |
| B-DT | Digital twin | `"digital twin*" OR "cyber-physical system*" OR "virtual replica*"` |
| B-UAV | UAV photogrammetry | `UAV OR UAS OR drone* OR "unmanned aerial" OR "remotely piloted aircraft"` |
| B-PHO | Photogrammetry products | `photogrammetr* OR "structure from motion" OR "structure-from-motion" OR orthophoto* OR orthomosaic* OR DSM OR DEM OR DTM OR "point cloud*" OR "digital surface model*" OR "digital elevation model*"` |
| B-QTY | Quantity / progress / payment | `"progress monitoring" OR "progress measurement" OR "progress tracking" OR "quantity takeoff" OR "quantity take-off" OR "quantity surveying" OR "earthwork volume*" OR "volume calculation" OR "progress payment*" OR "interim payment*" OR invoic* OR "payment application*" OR "payment certif*"` |
| B-SUB | Subcontractor / commercial | `subcontract* OR "quantity surveyor*" OR claim* OR dispute* OR "payment delay*" OR "commercial management" OR "contract administration"` |

## 3. Core combined string (CORE-01)
The CORE string targets the intersection of the review: linear or oil-and-gas construction, a digital twin or UAV technology, and quantity, progress or payment.

**Scopus**
```
TITLE-ABS-KEY(
  ( pipeline* OR "linear infrastructure" OR "linear project*" OR "right-of-way" OR "right of way" OR corridor* OR "oil and gas" OR "gas pipeline*" OR "oil pipeline*" OR highway* OR railway* )
  AND ( "digital twin*" OR UAV OR UAS OR drone* OR "unmanned aerial" OR photogrammetr* OR orthophoto* OR "point cloud*" )
  AND ( "progress monitoring" OR "progress measurement" OR "progress tracking" OR "quantity takeoff" OR "quantity take-off" OR "earthwork volume*" OR "volume calculation" OR "progress payment*" OR invoic* OR subcontract* OR "quantity surveying" OR "as-built" )
  AND ( construction OR contractor* OR "construction site*" )
)
```

**Web of Science**
```
TS=( ( pipeline* OR "linear infrastructure" OR "linear project*" OR "right-of-way" OR "right of way" OR corridor* OR "oil and gas" OR "gas pipeline*" OR "oil pipeline*" OR highway* OR railway* )
  AND ( "digital twin*" OR UAV OR UAS OR drone* OR "unmanned aerial" OR photogrammetr* OR orthophoto* OR "point cloud*" )
  AND ( "progress monitoring" OR "progress measurement" OR "progress tracking" OR "quantity takeoff" OR "quantity take-off" OR "earthwork volume*" OR "volume calculation" OR "progress payment*" OR invoic* OR subcontract* OR "quantity surveying" OR "as-built" )
  AND ( construction OR contractor* OR "construction site*" ) )
```

## 4. Cluster strings
Each cluster string is combined with the construction context. Scopus syntax is shown first, then the Web of Science version. The WoS version replaces `TITLE-ABS-KEY(` with `TS=(`. Boolean, phrase and truncation syntax is the same, but WoS `NEAR/n` replaces Scopus `W/n`.

### C1: Digital twins in construction and oil & gas
```
TITLE-ABS-KEY( ( "digital twin*" OR "cyber-physical system*" ) AND ( construction OR "construction site*" OR "construction project*" OR "oil and gas" OR pipeline* OR "linear infrastructure" ) AND ( monitoring OR progress OR "site operation*" OR production OR management ) )
```
```
TS=( ( "digital twin*" OR "cyber-physical system*" ) AND ( construction OR "construction site*" OR "construction project*" OR "oil and gas" OR pipeline* OR "linear infrastructure" ) AND ( monitoring OR progress OR "site operation*" OR production OR management ) )
```

### C2: UAV photogrammetry, orthophotos, DEM/DSM, volumetrics
```
TITLE-ABS-KEY( ( UAV OR UAS OR drone* OR "unmanned aerial" ) AND ( photogrammetr* OR "structure from motion" OR orthophoto* OR orthomosaic* OR DSM OR DEM OR DTM OR "point cloud*" ) AND ( earthwork* OR volume* OR stockpile* OR excavat* OR "construction site*" OR survey* ) AND ( accuracy OR uncertainty OR "ground control point*" OR GCP OR RTK OR PPK OR validation ) )
```
```
TS=( ( UAV OR UAS OR drone* OR "unmanned aerial" ) AND ( photogrammetr* OR "structure from motion" OR orthophoto* OR orthomosaic* OR DSM OR DEM OR DTM OR "point cloud*" ) AND ( earthwork* OR volume* OR stockpile* OR excavat* OR "construction site*" OR survey* ) AND ( accuracy OR uncertainty OR "ground control point*" OR GCP OR RTK OR PPK OR validation ) )
```

### C3: BIM/GIS integration for linear infrastructure
```
TITLE-ABS-KEY( ( BIM OR "building information model*" OR "infrastructure information model*" ) W/15 ( GIS OR "geographic information" OR geospatial ) AND ( "linear infrastructure" OR pipeline* OR highway* OR road* OR railway* OR corridor* OR "linear referencing" OR chainage OR stationing OR alignment ) )
```
```
TS=( ( BIM OR "building information model*" OR "infrastructure information model*" ) NEAR/15 ( GIS OR "geographic information" OR geospatial ) AND ( "linear infrastructure" OR pipeline* OR highway* OR road* OR railway* OR corridor* OR "linear referencing" OR chainage OR stationing OR alignment ) )
```

### C4: Personnel and equipment tracking
```
TITLE-ABS-KEY( ( RFID OR BLE OR "bluetooth low energy" OR UWB OR "ultra-wideband" OR GNSS OR GPS OR telematics OR IoT OR "internet of things" OR wearable* OR "computer vision" OR "activity recognition" ) AND ( worker* OR labor OR labour OR crew* OR equipment OR machinery OR "heavy equipment" OR fleet ) AND ( "construction site*" OR "construction project*" OR construction ) AND ( tracking OR localization OR localisation OR monitoring OR productivity OR "idle time" ) )
```
```
TS=( ( RFID OR BLE OR "bluetooth low energy" OR UWB OR "ultra-wideband" OR GNSS OR GPS OR telematics OR IoT OR "internet of things" OR wearable* OR "computer vision" OR "activity recognition" ) AND ( worker* OR labor OR labour OR crew* OR equipment OR machinery OR "heavy equipment" OR fleet ) AND ( "construction site*" OR "construction project*" OR construction ) AND ( tracking OR localization OR localisation OR monitoring OR productivity OR "idle time" ) )
```

### C5: Productivity monitoring and earned value management
```
TITLE-ABS-KEY( ( "productivity monitoring" OR "productivity measurement" OR "labor productivity" OR "labour productivity" OR "equipment productivity" OR "earned value" OR EVM OR "schedule performance" ) AND ( construction OR contractor* OR "construction project*" ) AND ( automat* OR "real-time" OR "real time" OR sensor* OR "data-driven" OR dashboard* OR digital ) )
```
```
TS=( ( "productivity monitoring" OR "productivity measurement" OR "labor productivity" OR "labour productivity" OR "equipment productivity" OR "earned value" OR EVM OR "schedule performance" ) AND ( construction OR contractor* OR "construction project*" ) AND ( automat* OR "real-time" OR "real time" OR sensor* OR "data-driven" OR dashboard* OR digital ) )
```

### C6: Progress measurement, quantity takeoff, subcontractor administration, invoice verification
```
TITLE-ABS-KEY( ( "progress payment*" OR "interim payment*" OR "payment application*" OR "payment certif*" OR invoic* OR "quantity takeoff" OR "quantity take-off" OR "quantity surveying" OR "measurement of work*" OR "progress measurement" OR "as-built quantit*" ) AND ( subcontract* OR contractor* OR "construction project*" OR construction ) AND ( automat* OR verif* OR digital OR dispute* OR claim* OR "payment delay*" OR blockchain OR "smart contract*" ) )
```
```
TS=( ( "progress payment*" OR "interim payment*" OR "payment application*" OR "payment certif*" OR invoic* OR "quantity takeoff" OR "quantity take-off" OR "quantity surveying" OR "measurement of work*" OR "progress measurement" OR "as-built quantit*" ) AND ( subcontract* OR contractor* OR "construction project*" OR construction ) AND ( automat* OR verif* OR digital OR dispute* OR claim* OR "payment delay*" OR blockchain OR "smart contract*" ) )
```

### C7: Data interoperability and standards
```
TITLE-ABS-KEY( ( IFC OR "industry foundation classes" OR LandXML OR "ISO 19650" OR "OPC UA" OR "OGC" OR CityGML OR "3D Tiles" OR PODS OR "pipeline open data standard" OR "ISO 15143" OR "AEMP" OR "linked data" OR ontolog* OR API* ) AND ( interoperab* OR integration OR "data exchange" OR schema ) AND ( construction OR infrastructure OR pipeline* OR "digital twin*" ) )
```
```
TS=( ( IFC OR "industry foundation classes" OR LandXML OR "ISO 19650" OR "OPC UA" OR "OGC" OR CityGML OR "3D Tiles" OR PODS OR "pipeline open data standard" OR "ISO 15143" OR "AEMP" OR "linked data" OR ontolog* OR API* ) AND ( interoperab* OR integration OR "data exchange" OR schema ) AND ( construction OR infrastructure OR pipeline* OR "digital twin*" ) )
```
**[A] A-022.** The token `API*` may produce noise (for example, the American Petroleum Institute in oil-and-gas papers). If the pilot shows that, drop it or replace it with `"application programming interface*"`.

### C8: Data quality, uncertainty, validation, auditability
```
TITLE-ABS-KEY( ( "data quality" OR "measurement uncertainty" OR uncertaint* W/3 (measurement OR volume* OR quantit*) OR "data validation" OR provenance OR "audit trail" OR auditab* OR traceab* OR "data integrity" ) AND ( construction OR "construction site*" OR "digital twin*" OR "progress monitoring" OR survey* ) )
```
```
TS=( ( "data quality" OR "measurement uncertainty" OR uncertaint* NEAR/3 (measurement OR volume* OR quantit*) OR "data validation" OR provenance OR "audit trail" OR auditab* OR traceab* OR "data integrity" ) AND ( construction OR "construction site*" OR "digital twin*" OR "progress monitoring" OR survey* ) )
```

### C9: Change management and technology adoption
```
TITLE-ABS-KEY( ( "technology adoption" OR "technology acceptance" OR TAM OR UTAUT OR "diffusion of innovation*" OR "resistance to change" OR "change management" OR "digital transformation" ) AND ( construction OR contractor* OR "construction industry" OR "construction site*" ) AND ( digital OR BIM OR "digital twin*" OR drone* OR UAV OR IoT OR wearable* OR tracking OR "mobile app*" ) )
```
```
TS=( ( "technology adoption" OR "technology acceptance" OR TAM OR UTAUT OR "diffusion of innovation*" OR "resistance to change" OR "change management" OR "digital transformation" ) AND ( construction OR contractor* OR "construction industry" OR "construction site*" ) AND ( digital OR BIM OR "digital twin*" OR drone* OR UAV OR IoT OR wearable* OR tracking OR "mobile app*" ) )
```

### C4-ETH: worker-tracking ethics and privacy (supplementary)
```
TITLE-ABS-KEY( ( privacy OR ethic* OR surveillance OR consent OR GDPR ) AND ( tracking OR wearable* OR localization OR "location data" OR monitoring ) AND ( worker* OR employee* OR labour OR labor ) AND ( construction OR "construction site*" OR industrial ) )
```

## 5. Google Scholar and institutional sources

### Google Scholar
- Scholar does not support truncation or long Boolean nesting, so the strings are shortened.
- Run each string in a private session with **"since 2010"** set. Screen **only the first 200 results sorted by relevance** for each string. This follows common SLR practice, because ranking reproducibility is limited.
- Export with Publish or Perish where possible, and record the run date.

| ID | String |
|---|---|
| GS-01 | `"digital twin" pipeline construction progress quantity` |
| GS-02 | `UAV photogrammetry pipeline right-of-way earthwork volume accuracy` |
| GS-03 | `drone "progress payment" OR "quantity verification" construction subcontractor` |
| GS-04 | `"linear referencing" OR chainage BIM GIS pipeline construction` |
| GS-05 | `construction equipment telematics worker tracking productivity "linear project"` |
| GS-06 | `"subcontractor payment" OR "interim payment" automation dispute construction` |
| GS-07 | `"digital twin" "oil and gas" construction phase` |

### POLIMI institutional sources
| ID | Source | Query approach |
|---|---|---|
| PM-01 | **POLITesi** (POLIMI theses) | Keyword search, each separately: `digital twin cantiere`, `digital twin construction`, `drone fotogrammetria`, `UAV photogrammetry`, `pipeline`, `avanzamento lavori` (progress), `contabilità lavori` (works accounting), `SAL` (stato avanzamento lavori), `BIM GIS infrastrutture lineari`. Filter to the Management Engineering, Building/Construction Engineering and Geoinformatics programmes. Years 2015–2026. |
| PM-02 | **RE.PUBLIC@POLIMI** (institutional research repository) | `digital twin AND construction`; `UAV AND (photogrammetry OR survey)`; `BIM AND GIS`; `construction AND (progress OR productivity)`. Use this to identify POLIMI research groups and potential co-authors. |
| PM-03 | **POLIMI library discovery service** | Use the CORE-01 terms in simplified form, to retrieve books and standards and to check full-text access (supports the EX6 exclusion). |

**[R]** Italian terms ("SAL", "contabilità lavori", "computo metrico", "libretto delle misure") capture the Italian works-accounting tradition, which is directly relevant to quantity certification.

## 6. Search log template
Save it as `search_log.csv` in Phase 2.

```csv
run_date,database,string_id,string_version,hits_raw,hits_after_limits,exported,export_file,notes
2027-01-04,Scopus,CORE-01,v1.0,,,,,EXAMPLE ROW - replace
```

| Column | Meaning |
|---|---|
| `string_id` | CORE-01, C1…C9, C4-ETH, GS-01…07, PM-01…03 |
| `string_version` | Increment the version whenever a string is edited after piloting |

## 7. Gold-set test
Before freezing the strings, check that CORE-01 or the relevant cluster string retrieves the seed works indexed in Scopus or WoS. Examples: Siebert & Teizer (2014) for C2; Omar & Nehdi (2016) for C6; Boje et al. (2020) for C1.

**[R]** If more than 20% of the gold set is missed, broaden the string.
