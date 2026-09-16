#!/usr/bin/env python3
"""Supplier discovery scraper for B2B directories.

Searches a directory for a keyword, walks the result pages, opens every company
profile and writes a clean vendor CSV.

Design notes
------------
* robots.txt is enforced before every fetch and its Crawl-delay is honoured.
  Disallowed URLs are skipped and logged, never fetched.
* Requests-first, Playwright-on-demand: static HTML is cheaper and politer, so
  the browser only spins up when the static fetch returns nothing usable.
* Extraction is layered - CSS selectors from the site profile first, then
  JSON-LD (schema.org Organization/LocalBusiness), then microdata, then
  mailto:/tel: links and text regexes. A selector going stale degrades the row,
  it does not empty it.
* Missing fields are written as "" (never null/NaN), per spec.

Usage
-----
    python scraper.py                       # uses .env / defaults
    python scraper.py --keyword "welding services" --domain europages.co.uk
    python scraper.py --inspect             # dump live DOM structure, no scrape
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import random
import re
import sys
import time
import urllib.parse as urlparse
import urllib.robotparser as robotparser
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from site_profiles import SiteProfile, profile_for

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

FIELDS = [
    "company_name",
    "website_url",
    "contact_email",
    "contact_phone",
    "address_line",
    "city",
    "postal_code",
    "country",
    "profile_url",
    "categories_or_services",
    "certifications_or_standards",
    "marketplace_id_or_internal_id",
    "last_scraped_at",
]

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36 SupplierDiscoveryBot/1.0 (+contact: procurement)"
)
ROBOTS_AGENT = "SupplierDiscoveryBot"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+|00)\d[\d\s().\-/]{6,20}\d")
POSTCODE_CITY_RE = re.compile(
    r"\b(?P<postal>(?:[A-Z]{1,2}-)?\d{4,6}|[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\s+(?P<city>[A-ZÀ-Ý][\w'\-\. ]{1,40})"
)
CERT_RE = re.compile(
    r"\b(?:ISO\s?/?\s?(?:IEC|TS|TR)?\s?\d{3,5}(?:[:\-]\d{1,4})?"
    r"|EN\s?\d{3,5}(?:[\-\s]\d+)?"
    r"|IATF\s?\d{4,5}"
    r"|OHSAS\s?\d{4,5}"
    r"|API\s?(?:Q1|Q2|\d[A-Z]?)"
    r"|ASME\s?[IVXU]+"
    r"|AD\s?2000"
    r"|CE\b|ATEX\b|SCC\*?\*?|PED\b)",
    re.IGNORECASE,
)
# Hosts that are never the vendor's own website.
SOCIAL_HOSTS = (
    "facebook.", "twitter.", "x.com", "linkedin.", "instagram.", "youtube.",
    "pinterest.", "tiktok.", "xing.", "wa.me", "whatsapp.", "google.",
)

LOG = logging.getLogger("supplier_scraper")


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #

@dataclass
class Config:
    keyword: str
    domain: str
    max_pages: int
    output: str
    engine: str
    delay_min: float
    delay_max: float
    respect_robots: bool
    search_url_template: str
    playwright_executable_path: str
    max_profiles: int
    inspect: bool

    @property
    def scheme_host(self) -> str:
        host = self.domain.split("//")[-1].strip("/")
        scheme = "http" if host.startswith(("127.0.0.1", "localhost")) else "https"
        return f"{scheme}://{host}"


def _env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def build_config(argv: Optional[List[str]] = None) -> Config:
    load_dotenv()
    p = argparse.ArgumentParser(description="B2B directory supplier discovery scraper")
    p.add_argument("--keyword", default=_env("KEYWORD", "welding services"))
    p.add_argument("--domain", default=_env("TARGET_DOMAIN", "europages.co.uk"))
    p.add_argument("--max-pages", type=int, default=int(_env("MAX_PAGES", "3") or 3))
    p.add_argument("--output", default=_env("OUTPUT", "vendors.csv"))
    p.add_argument("--engine", choices=("auto", "requests", "playwright"),
                   default=_env("ENGINE", "auto") or "auto")
    p.add_argument("--delay-min", type=float, default=float(_env("DELAY_MIN", "1.5") or 1.5))
    p.add_argument("--delay-max", type=float, default=float(_env("DELAY_MAX", "2.5") or 2.5))
    p.add_argument("--ignore-robots", action="store_true",
                   help="Do not use this on a site you do not own.")
    p.add_argument("--search-url-template", default=_env("SEARCH_URL_TEMPLATE"))
    p.add_argument("--max-profiles", type=int, default=int(_env("MAX_PROFILES", "0") or 0))
    p.add_argument("--inspect", action="store_true",
                   help="Fetch page 1 + one profile and print their structure, then exit.")
    a = p.parse_args(argv)

    respect = _env("RESPECT_ROBOTS", "true").lower() not in ("false", "0", "no")
    if a.ignore_robots:
        respect = False

    return Config(
        keyword=a.keyword,
        domain=a.domain.split("//")[-1].strip("/"),
        max_pages=max(1, a.max_pages),
        output=a.output,
        engine=a.engine,
        delay_min=a.delay_min,
        delay_max=max(a.delay_max, a.delay_min),
        respect_robots=respect,
        search_url_template=a.search_url_template,
        playwright_executable_path=_env("PLAYWRIGHT_EXECUTABLE_PATH"),
        max_profiles=a.max_profiles,
        inspect=a.inspect,
    )


# --------------------------------------------------------------------------- #
# robots.txt
# --------------------------------------------------------------------------- #

class RobotsGate:
    """Caches one RobotFileParser per host. Fail-closed on parse errors."""

    def __init__(self, enabled: bool, session: requests.Session):
        self.enabled = enabled
        self.session = session
        self._parsers: Dict[str, Optional[robotparser.RobotFileParser]] = {}
        self._unreachable: set = set()

    def _parser(self, url: str) -> Optional[robotparser.RobotFileParser]:
        parts = urlparse.urlsplit(url)
        root = f"{parts.scheme}://{parts.netloc}"
        if root in self._parsers:
            return self._parsers[root]
        rp = robotparser.RobotFileParser()
        rp.set_url(root + "/robots.txt")
        try:
            kwargs = {"timeout": 20, "headers": {"User-Agent": USER_AGENT}}
            if urlparse.urlsplit(root).hostname in ("127.0.0.1", "localhost"):
                kwargs["proxies"] = {"http": None, "https": None}
            resp = self.session.get(root + "/robots.txt", **kwargs)
            if resp.status_code >= 400:
                # No robots.txt published -> nothing is disallowed.
                rp.parse([])
                LOG.info("robots.txt for %s returned HTTP %s; treating as allow-all",
                         root, resp.status_code)
            else:
                rp.parse(resp.text.splitlines())
                LOG.info("robots.txt loaded for %s (%d bytes)", root, len(resp.text))
        except Exception as exc:  # network/proxy/DNS failure
            self._unreachable.add(root)
            LOG.error("robots.txt for %s unreachable (%s) - refusing to crawl this host",
                      root, exc)
            self._parsers[root] = None
            return None
        self._parsers[root] = rp
        return rp

    def check(self, url: str) -> Tuple[bool, str]:
        """(allowed, reason-if-not). Unknown policy fails closed."""
        if not self.enabled:
            return True, ""
        rp = self._parser(url)
        if rp is None:
            return False, ("robots.txt unreachable - host blocked by network policy, "
                           "offline, or refusing our requests; failing closed")
        try:
            ok = rp.can_fetch(ROBOTS_AGENT, url) or rp.can_fetch("*", url)
        except Exception as exc:
            return False, f"robots.txt could not be evaluated ({exc}); failing closed"
        return ok, "" if ok else "robots.txt disallows this path"

    def allowed(self, url: str) -> bool:
        return self.check(url)[0]

    def crawl_delay(self, url: str) -> float:
        if not self.enabled:
            return 0.0
        rp = self._parser(url)
        if rp is None:
            return 0.0
        for agent in (ROBOTS_AGENT, "*"):
            try:
                d = rp.crawl_delay(agent)
            except Exception:
                d = None
            if d:
                return float(d)
        return 0.0


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #

class FetchError(Exception):
    pass


class RequestsFetcher:
    name = "requests"

    def __init__(self, session: requests.Session):
        self.session = session

    def get(self, url: str, timeout: int = 30) -> str:
        kwargs = {"timeout": timeout, "headers": {"User-Agent": USER_AGENT,
                                                  "Accept-Language": "en,de;q=0.8,it;q=0.6"}}
        if urlparse.urlsplit(url).hostname in ("127.0.0.1", "localhost"):
            kwargs["proxies"] = {"http": None, "https": None}
        resp = self.session.get(url, **kwargs)
        if resp.status_code >= 400:
            raise FetchError(f"HTTP {resp.status_code}", )
        return resp.text

    def close(self):
        self.session.close()


class PlaywrightFetcher:
    name = "playwright"

    def __init__(self, executable_path: str = ""):
        from playwright.sync_api import sync_playwright  # imported lazily
        self._pw = sync_playwright().start()
        launch: Dict = {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
        if executable_path:
            launch["executable_path"] = executable_path
        try:
            self._browser = self._pw.chromium.launch(**launch)
        except Exception:
            # Common on hosts with a pre-baked browser that the pinned
            # Playwright build does not recognise.
            for guess in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                          "/usr/bin/chromium", "/usr/bin/google-chrome"):
                if os.path.exists(guess):
                    launch["executable_path"] = guess
                    self._browser = self._pw.chromium.launch(**launch)
                    break
            else:
                raise
        self._ctx = self._browser.new_context(user_agent=USER_AGENT,
                                              locale="en-GB",
                                              viewport={"width": 1366, "height": 900})
        self._page = self._ctx.new_page()

    def get(self, url: str, timeout: int = 45) -> str:
        resp = self._page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        if resp is not None and resp.status >= 400:
            raise FetchError(f"HTTP {resp.status}")
        try:
            self._page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass  # networkidle never settles on ad-heavy pages; the DOM is enough
        return self._page.content()

    def close(self):
        for closer in (self._ctx.close, self._browser.close, self._pw.stop):
            try:
                closer()
            except Exception:
                pass


class Crawler:
    """Rate limiting + retries + robots enforcement around a fetcher."""

    def __init__(self, fetcher, robots: RobotsGate, delay_min: float, delay_max: float):
        self.fetcher = fetcher
        self.robots = robots
        self.delay_min = delay_min
        self.delay_max = delay_max
        self._last_fetch = 0.0
        self.skipped: List[Tuple[str, str]] = []
        self.fetched = 0

    def _sleep(self, url: str) -> None:
        wait = random.uniform(self.delay_min, self.delay_max)
        wait = max(wait, self.robots.crawl_delay(url))
        elapsed = time.monotonic() - self._last_fetch
        if elapsed < wait:
            time.sleep(wait - elapsed)

    def get(self, url: str, attempts: int = 3) -> Optional[str]:
        ok, why = self.robots.check(url)
        if not ok:
            self.skipped.append((url, why))
            LOG.warning("SKIP (%s): %s", why, url)
            return None
        backoff = 2.0
        for attempt in range(1, attempts + 1):
            self._sleep(url)
            self._last_fetch = time.monotonic()
            try:
                html = self.fetcher.get(url)
                self.fetched += 1
                LOG.info("GET  %s (%d bytes)", url, len(html))
                return html
            except Exception as exc:
                msg = str(exc) or exc.__class__.__name__
                if attempt == attempts:
                    self.skipped.append((url, f"fetch failed after {attempts} attempts: {msg}"))
                    LOG.error("FAIL %s -> %s", url, msg)
                    return None
                LOG.warning("retry %d/%d for %s (%s); sleeping %.0fs",
                            attempt, attempts - 1, url, msg, backoff)
                time.sleep(backoff)
                backoff *= 2
        return None

    def close(self):
        self.fetcher.close()


# --------------------------------------------------------------------------- #
# Extraction helpers
# --------------------------------------------------------------------------- #

def soup_of(html: str) -> BeautifulSoup:
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def clean(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def select_first(node, selectors: Iterable[str]):
    for sel in selectors:
        try:
            hit = node.select_one(sel)
        except Exception:
            continue  # malformed selector - keep going
        if hit is not None:
            return hit
    return None


def select_text(node, selectors: Iterable[str]) -> str:
    hit = select_first(node, selectors)
    if hit is None:
        return ""
    if hit.name == "meta":
        return clean(hit.get("content", ""))
    return clean(hit.get_text(" ", strip=True))


def select_all_text(node, selectors: Iterable[str], limit: int = 25) -> List[str]:
    out: List[str] = []
    for sel in selectors:
        try:
            hits = node.select(sel)
        except Exception:
            continue
        for h in hits:
            t = clean(h.get_text(" ", strip=True))
            if t and t not in out:
                out.append(t)
            if len(out) >= limit:
                return out
        if out:
            return out
    return out


def jsonld_blocks(soup: BeautifulSoup) -> List[dict]:
    """Every schema.org object on the page, flattened out of @graph/lists."""
    blocks: List[dict] = []

    def walk(obj):
        if isinstance(obj, dict):
            if "@graph" in obj:
                walk(obj["@graph"])
            blocks.append(obj)
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = tag.string or tag.get_text() or ""
        try:
            walk(json.loads(raw))
        except Exception:
            continue
    return blocks


ORG_TYPES = {"organization", "localbusiness", "corporation", "company",
             "manufacturer", "professionalservice", "store", "wholesalestore"}


def org_from_jsonld(soup: BeautifulSoup) -> dict:
    """Best organisation-ish JSON-LD block, normalised to our field names."""
    best: dict = {}
    for block in jsonld_blocks(soup):
        types = block.get("@type", "")
        types = [types] if isinstance(types, str) else types
        if not any(str(t).lower() in ORG_TYPES for t in types):
            continue
        addr = block.get("address") or {}
        if isinstance(addr, list):
            addr = addr[0] if addr else {}
        if isinstance(addr, str):
            addr = {"streetAddress": addr}
        contact = block.get("contactPoint") or {}
        if isinstance(contact, list):
            contact = contact[0] if contact else {}

        country = addr.get("addressCountry", "")
        if isinstance(country, dict):
            country = country.get("name", "")

        cand = {
            "company_name": clean(str(block.get("name", "") or "")),
            "website_url": clean(str(block.get("url", "") or "")),
            "contact_email": clean(str(block.get("email", "") or contact.get("email", "") or "")),
            "contact_phone": clean(str(block.get("telephone", "") or contact.get("telephone", "") or "")),
            "address_line": clean(str(addr.get("streetAddress", "") or "")),
            "city": clean(str(addr.get("addressLocality", "") or "")),
            "postal_code": clean(str(addr.get("postalCode", "") or "")),
            "country": clean(str(country or "")),
            "marketplace_id_or_internal_id": clean(str(
                block.get("identifier", "") or block.get("@id", "") or "")),
        }
        kw = block.get("keywords") or block.get("knowsAbout") or ""
        if isinstance(kw, list):
            cand["categories_or_services"] = ", ".join(clean(str(k)) for k in kw if clean(str(k)))
        elif kw:
            cand["categories_or_services"] = clean(str(kw))
        # Keep the richest block seen.
        if sum(1 for v in cand.values() if v) > sum(1 for v in best.values() if v):
            best = cand
    return best


def microdata(soup: BeautifulSoup) -> dict:
    out = {}
    mapping = {
        "name": "company_name", "email": "contact_email", "telephone": "contact_phone",
        "streetAddress": "address_line", "addressLocality": "city",
        "postalCode": "postal_code", "addressCountry": "country", "url": "website_url",
    }
    for prop, fieldname in mapping.items():
        tag = soup.select_one(f"[itemprop='{prop}']")
        if tag is None:
            continue
        val = tag.get("content") or tag.get("href") or tag.get_text(" ", strip=True)
        val = clean(val)
        if val.startswith("mailto:"):
            val = val[7:]
        if val.startswith("tel:"):
            val = val[4:]
        if val:
            out[fieldname] = val
    return out


def external_website(soup: BeautifulSoup, directory_host: str) -> str:
    """First outbound link that is not the directory itself or a social network."""
    for a in soup.select("a[href^='http']"):
        href = a.get("href", "")
        host = (urlparse.urlsplit(href).hostname or "").lower()
        if not host or directory_host in host or host in directory_host:
            continue
        if any(s in host for s in SOCIAL_HOSTS):
            continue
        return href.split("?")[0]
    return ""


def guess_country(domain: str) -> str:
    tld = domain.lower().rstrip("/").split(":")[0].rsplit(".", 1)[-1]
    return {
        "de": "Germany", "it": "Italy", "fr": "France", "es": "Spain",
        "nl": "Netherlands", "pl": "Poland", "at": "Austria", "ch": "Switzerland",
        "uk": "United Kingdom", "be": "Belgium", "pt": "Portugal", "se": "Sweden",
    }.get(tld, "")


# --------------------------------------------------------------------------- #
# Page parsers
# --------------------------------------------------------------------------- #

def parse_results_page(html: str, page_url: str, prof: SiteProfile) -> Tuple[List[dict], str]:
    """Return (result stubs, absolute next-page URL or '')."""
    soup = soup_of(html)
    cards = []
    for sel in prof.result_card:
        try:
            found = soup.select(sel)
        except Exception:
            continue
        if found:
            cards = found
            LOG.debug("result cards matched by selector %r (%d)", sel, len(found))
            break

    stubs: List[dict] = []
    seen_links = set()
    for card in cards:
        link = select_first(card, prof.profile_link)
        href = link.get("href") if link is not None else None
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        abs_url = urlparse.urljoin(page_url, href).split("#")[0]
        if abs_url in seen_links or abs_url.rstrip("/") == page_url.rstrip("/"):
            continue
        seen_links.add(abs_url)
        internal_id = ""
        for attr_sel in prof.p_internal_id:
            attr = attr_sel.strip("[]").split("=")[0]
            if card.has_attr(attr):
                internal_id = clean(str(card[attr]))
                break
        stubs.append({
            "profile_url": abs_url,
            "company_name": select_text(card, prof.card_name) or clean(link.get_text(" ", strip=True)),
            "city": select_text(card, prof.card_city),
            "marketplace_id_or_internal_id": internal_id,
        })

    next_url = ""
    nxt = select_first(soup, prof.next_page)
    if nxt is not None and nxt.get("href"):
        candidate = urlparse.urljoin(page_url, nxt["href"]).split("#")[0]
        if candidate.rstrip("/") != page_url.rstrip("/"):
            next_url = candidate
    return stubs, next_url


def parse_profile_page(html: str, url: str, prof: SiteProfile, cfg: Config) -> dict:
    soup = soup_of(html)
    directory_host = (urlparse.urlsplit(url).hostname or cfg.domain).lower()
    row = {f: "" for f in FIELDS}
    row["profile_url"] = url

    # Layer 1 - structured data (most reliable when present).
    row.update({k: v for k, v in org_from_jsonld(soup).items() if v})
    for k, v in microdata(soup).items():
        row.setdefault(k, "")
        if not row[k]:
            row[k] = v

    # A directory's own JSON-LD often puts the directory URL in "url" - that is
    # not the vendor's website, and neither is a social profile.
    if row.get("website_url"):
        whost = (urlparse.urlsplit(row["website_url"]).hostname or "").lower()
        if (not whost or directory_host in whost or whost in directory_host
                or any(sh in whost for sh in SOCIAL_HOSTS)):
            row["website_url"] = ""

    # Layer 2 - site profile CSS selectors.
    def fill(key: str, value: str):
        if value and not row.get(key):
            row[key] = value

    fill("company_name", select_text(soup, prof.p_name))
    fill("city", select_text(soup, prof.p_city))
    fill("postal_code", select_text(soup, prof.p_postal_code))
    fill("country", select_text(soup, prof.p_country))
    fill("address_line", select_text(soup, prof.p_address))

    mail = select_first(soup, prof.p_email)
    if mail is not None:
        val = mail.get("href", "") or mail.get("content", "") or mail.get_text(strip=True)
        fill("contact_email", clean(val.replace("mailto:", "").split("?")[0]))
    tel = select_first(soup, prof.p_phone)
    if tel is not None:
        val = tel.get("href", "") or tel.get("content", "") or tel.get_text(strip=True)
        fill("contact_phone", clean(val.replace("tel:", "")))

    site = select_first(soup, prof.p_website)
    if site is not None and site.get("href", "").startswith("http"):
        host = (urlparse.urlsplit(site["href"]).hostname or "").lower()
        if directory_host not in host and not any(s in host for s in SOCIAL_HOSTS):
            fill("website_url", site["href"].split("?")[0])

    cats = select_all_text(soup, prof.p_categories)
    if cats and not row["categories_or_services"]:
        row["categories_or_services"] = ", ".join(dict.fromkeys(cats))

    # Layer 3 - regex / link fallbacks over the whole page.
    page_text = soup.get_text(" ", strip=True)

    if not row["contact_email"]:
        a = soup.select_one("a[href^='mailto:']")
        if a is not None:
            row["contact_email"] = clean(a["href"][7:].split("?")[0])
        else:
            m = EMAIL_RE.search(page_text)
            if m:
                row["contact_email"] = m.group(0)
    if not row["contact_phone"]:
        a = soup.select_one("a[href^='tel:']")
        if a is not None:
            row["contact_phone"] = clean(a["href"][4:])
        else:
            m = PHONE_RE.search(page_text)
            if m:
                row["contact_phone"] = clean(m.group(0))
    if not row["website_url"]:
        row["website_url"] = external_website(soup, directory_host)

    if row["address_line"] and not all((row["city"], row["postal_code"], row["country"])):
        segments = [seg.strip() for seg in row["address_line"].split(",") if seg.strip()]
        if not row["country"] and len(segments) >= 2:
            tail = segments[-1]
            if not any(ch.isdigit() for ch in tail) and 2 < len(tail) <= 40:
                row["country"] = tail
        m = POSTCODE_CITY_RE.search(row["address_line"])
        if m:
            if not row["postal_code"]:
                row["postal_code"] = clean(m.group("postal"))
            if not row["city"]:
                row["city"] = clean(m.group("city"))
            # Keep address_line as the street line only; the rest has its own columns.
            street = row["address_line"][: m.start()].strip(" ,;")
            if street:
                row["address_line"] = street
    if not row["country"]:
        row["country"] = guess_country(cfg.domain)

    certs = select_all_text(soup, prof.p_certifications, limit=10)
    found_certs: List[str] = []
    for chunk in certs + [page_text]:
        for m in CERT_RE.finditer(chunk):
            token = re.sub(r"\s+", " ", m.group(0).upper().replace(" /", "/"))
            if token not in found_certs:
                found_certs.append(token)
        if found_certs:
            break
    row["certifications_or_standards"] = ", ".join(found_certs[:12])

    if not row["marketplace_id_or_internal_id"]:
        for attr_sel in prof.p_internal_id:
            attr = attr_sel.strip("[]").split("=")[0]
            tag = soup.select_one(f"[{attr}]")
            if tag is not None:
                row["marketplace_id_or_internal_id"] = clean(str(tag[attr]))
                break
        else:
            slug = urlparse.urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
            row["marketplace_id_or_internal_id"] = slug

    row["last_scraped_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return row


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #

def dedupe(rows: List[dict], domain: str) -> List[dict]:
    """Deduplicate on (directory domain + normalised company name)."""
    seen: Dict[Tuple[str, str], dict] = {}
    order: List[Tuple[str, str]] = []
    for row in rows:
        host = (urlparse.urlsplit(row.get("profile_url", "")).hostname or domain).lower()
        name = re.sub(r"[^a-z0-9]+", "", (row.get("company_name") or "").lower())
        key = (host, name or row.get("profile_url", ""))
        if key in seen:
            # Keep whichever record carries more populated fields.
            if sum(1 for v in row.values() if v) > sum(1 for v in seen[key].values() if v):
                seen[key] = row
            continue
        seen[key] = row
        order.append(key)
    return [seen[k] for k in order]


def write_csv(rows: List[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            writer.writerow({f: (row.get(f) or "") for f in FIELDS})


def make_fetcher(engine: str, cfg: Config, session: requests.Session):
    if engine == "playwright":
        return PlaywrightFetcher(cfg.playwright_executable_path)
    return RequestsFetcher(session)


def inspect(cfg: Config, prof: SiteProfile, crawler: Crawler, first_url: str) -> int:
    """Print enough of the live DOM to correct site_profiles.py."""
    html = crawler.get(first_url)
    if html is None:
        print(f"\nCould not fetch {first_url}. See the log above for the reason.")
        return 2
    soup = soup_of(html)
    print(f"\n=== SEARCH PAGE: {first_url} ===")
    print(f"title: {clean(soup.title.get_text()) if soup.title else '(none)'}")
    print("\n-- repeated block candidates (likely result cards) --")
    counts: Dict[str, int] = {}
    for tag in soup.find_all(["article", "li", "div"]):
        cls = ".".join(tag.get("class", [])[:3])
        if not cls:
            continue
        key = f"{tag.name}.{cls}"
        counts[key] = counts.get(key, 0) + 1
    for key, n in sorted(counts.items(), key=lambda kv: -kv[1])[:15]:
        if n >= 3:
            print(f"  {n:>4}x  {key}")
    print("\n-- pagination candidates --")
    for a in soup.select("a[rel], a[class*='next'], a[class*='pag'], a[aria-label]")[:15]:
        print(f"  <a class={a.get('class')} rel={a.get('rel')} "
              f"aria-label={a.get('aria-label')!r} href={a.get('href')}>")
    stubs, next_url = parse_results_page(html, first_url, prof)
    print(f"\ncurrent profile '{prof.name}' matched {len(stubs)} cards; next={next_url or '(none)'}")
    for s in stubs[:5]:
        print(f"  - {s['company_name'] or '(no name)'} -> {s['profile_url']}")
    if stubs:
        purl = stubs[0]["profile_url"]
        phtml = crawler.get(purl)
        if phtml:
            psoup = soup_of(phtml)
            print(f"\n=== PROFILE PAGE: {purl} ===")
            print(f"json-ld org blocks: {len(jsonld_blocks(psoup))}")
            print(f"json-ld extraction: {json.dumps(org_from_jsonld(psoup), indent=2)[:900]}")
            print(f"mailto links: {[a.get('href') for a in psoup.select('a[href^=mailto]')][:3]}")
            print(f"tel links:    {[a.get('href') for a in psoup.select('a[href^=tel]')][:3]}")
            print(f"h1:           {clean(psoup.h1.get_text()) if psoup.h1 else '(none)'}")
            print("\nparsed row with current selectors:")
            print(json.dumps(parse_profile_page(phtml, purl, prof, cfg), indent=2))
    return 0


def run(cfg: Config) -> int:
    prof = profile_for(cfg.domain)
    keyword_q = urlparse.quote_plus(cfg.keyword)
    keyword_slug = urlparse.quote(cfg.keyword.strip().lower().replace(" ", "-"))

    if cfg.search_url_template:
        template = cfg.search_url_template
    else:
        template = prof.search_url_template
    # Europages-style path templates read better with the slug form.
    kw = keyword_slug if "{keyword}.html" in template or "/{keyword}" in template else keyword_q
    first_url = template.format(domain=cfg.domain, keyword=kw, page=1)

    LOG.info("keyword=%r domain=%s profile=%s max_pages=%d engine=%s robots=%s",
             cfg.keyword, cfg.domain, prof.name, cfg.max_pages, cfg.engine,
             "enforced" if cfg.respect_robots else "IGNORED (your call)")
    LOG.info("search URL: %s", first_url)

    session = requests.Session()
    robots = RobotsGate(cfg.respect_robots, session)

    engine = cfg.engine
    if engine == "auto":
        engine = "requests" if prof.engine != "playwright" else "playwright"
    crawler = Crawler(make_fetcher(engine, cfg, session), robots, cfg.delay_min, cfg.delay_max)

    try:
        if cfg.inspect:
            return inspect(cfg, prof, crawler, first_url)

        # ---- phase 1: walk the result pages -------------------------------
        stubs: List[dict] = []
        url = first_url
        pages_done = 0
        for page_no in range(1, cfg.max_pages + 1):
            html = crawler.get(url)
            if html is None:
                break
            page_stubs, next_url = parse_results_page(html, url, prof)

            # Static fetch found nothing -> the site is probably JS-rendered.
            if not page_stubs and page_no == 1 and cfg.engine == "auto" and crawler.fetcher.name == "requests":
                LOG.warning("no result cards in static HTML; retrying with Playwright")
                try:
                    crawler.fetcher.close()
                    crawler.fetcher = make_fetcher("playwright", cfg, session)
                    html = crawler.get(url)
                    if html:
                        page_stubs, next_url = parse_results_page(html, url, prof)
                except Exception as exc:
                    LOG.error("Playwright fallback unavailable: %s", exc)

            LOG.info("page %d: %d result cards", page_no, len(page_stubs))
            if not page_stubs:
                crawler.skipped.append((url, "no result cards matched the profile selectors"))
                break
            stubs.extend(page_stubs)
            pages_done = page_no
            if page_no == cfg.max_pages:
                break
            if not next_url:
                next_url = template.format(domain=cfg.domain, keyword=kw, page=page_no + 1)
                LOG.info("no 'next' link found; constructing page %d URL", page_no + 1)
            url = next_url

        # Dedupe stubs by profile URL before spending requests on them.
        unique_stubs: List[dict] = []
        seen_urls = set()
        for s in stubs:
            if s["profile_url"] in seen_urls:
                continue
            seen_urls.add(s["profile_url"])
            unique_stubs.append(s)
        if cfg.max_profiles:
            unique_stubs = unique_stubs[: cfg.max_profiles]

        # ---- phase 2: visit each profile ----------------------------------
        rows: List[dict] = []
        visited = 0
        for i, stub in enumerate(unique_stubs, 1):
            purl = stub["profile_url"]
            LOG.info("profile %d/%d: %s", i, len(unique_stubs), purl)
            phtml = crawler.get(purl)
            if phtml is None:
                continue
            visited += 1
            try:
                row = parse_profile_page(phtml, purl, prof, cfg)
            except Exception as exc:
                crawler.skipped.append((purl, f"parse error: {exc}"))
                LOG.exception("parse error on %s", purl)
                continue
            # Results-page values are a fallback for anything the profile lacks.
            for key in ("company_name", "city", "marketplace_id_or_internal_id"):
                if not row.get(key) and stub.get(key):
                    row[key] = stub[key]
            if not row["company_name"]:
                crawler.skipped.append((purl, "no company name found"))
                LOG.warning("SKIP (no company name): %s", purl)
                continue
            rows.append(row)

        unique_rows = dedupe(rows, cfg.domain)
        write_csv(unique_rows, cfg.output)

        # ---- summary -------------------------------------------------------
        print("\n" + "=" * 68)
        print("SCRAPE SUMMARY")
        print("=" * 68)
        print(f"  keyword                : {cfg.keyword}")
        print(f"  directory              : {cfg.domain}  (profile: {prof.name})")
        print(f"  result pages walked    : {pages_done}")
        print(f"  profile URLs found     : {len(unique_stubs)}")
        print(f"  profile pages visited  : {visited}")
        print(f"  unique vendors saved   : {len(unique_rows)}  -> {cfg.output}")
        print(f"  duplicates collapsed   : {len(rows) - len(unique_rows)}")
        print(f"  skipped items          : {len(crawler.skipped)}")
        for u, why in crawler.skipped[:10]:
            print(f"      - {why}: {u}")
        if unique_rows:
            fill_rate = {
                f: sum(1 for r in unique_rows if r.get(f)) for f in FIELDS
            }
            print("\n  field fill rate:")
            for f in FIELDS:
                pct = 100 * fill_rate[f] / len(unique_rows)
                print(f"      {f:<32} {fill_rate[f]:>4}/{len(unique_rows)}  {pct:5.1f}%")
            print("\n  sample rows:")
            for row in unique_rows[:3]:
                print("      " + "-" * 58)
                for f in FIELDS:
                    print(f"      {f:<32}: {row.get(f, '')}")
        print("=" * 68)
        return 0 if unique_rows else 1
    finally:
        crawler.close()


def main() -> int:
    cfg = build_config()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler("scrape.log", encoding="utf-8")],
    )
    try:
        return run(cfg)
    except KeyboardInterrupt:
        LOG.warning("interrupted by user")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
