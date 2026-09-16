#!/usr/bin/env python3
"""A local stand-in for a B2B directory, used to test scraper.py end-to-end.

It deliberately reproduces the awkward parts of a real directory:
  * paginated results, with a rel=next link that disappears on the last page
  * a robots.txt Disallow that must be obeyed
  * a profile that 404s
  * three different markup styles - JSON-LD, microdata, plain HTML
  * the same company listed twice under different URLs
  * profiles with no e-mail, no website, or no certifications

    python tools/mock_site.py --port 8099
"""

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

VENDORS = [
    # slug, name, markup, city, postcode, street, country, phone, email, website, cats, certs
    ("nordwerk-schweisstechnik", "Nordwerk Schweißtechnik GmbH", "jsonld",
     "Hamburg", "22761", "Ottenser Hauptstraße 14", "Germany",
     "+49 40 5566 7788", "info@nordwerk-schweisstechnik.de", "https://www.nordwerk-schweisstechnik.de",
     ["Welding services", "Orbital welding", "Pipe fabrication"], "ISO 9001:2015, ISO 3834-2, EN 1090-2"),
    ("rheinstahl-montage", "Rheinstahl Montage AG", "microdata",
     "Duisburg", "47051", "Hafenstraße 88", "Germany",
     "+49 203 1122 334", "kontakt@rheinstahl-montage.de", "https://rheinstahl-montage.de",
     ["Steel structures", "Site welding", "Mechanical erection"], "ISO 9001, ISO 45001"),
    ("sudmetall-werke", "Südmetall Werke KG", "plain",
     "Augsburg", "86153", "Industriestraße 5", "Germany",
     "+49 821 445 6677", "", "https://www.suedmetall-werke.de",
     ["Sheet metal welding", "TIG welding"], ""),
    ("blocked-vendor", "Blocked Vendor GmbH", "plain",
     "Berlin", "10115", "Chausseestraße 1", "Germany",
     "+49 30 1111 2222", "x@blocked.de", "https://blocked.de", ["Welding"], ""),
    ("adria-saldature", "Adria Saldature S.r.l.", "jsonld",
     "Trieste", "34143", "Via del Porto 22", "Italy",
     "+39 040 332 4455", "commerciale@adriasaldature.it", "",
     ["Servizi di saldatura", "Carpenteria metallica"], "ISO 9001:2015, ISO 3834-3"),
    ("missing-page", "Ghost Industries", "plain",
     "Köln", "50667", "Domstraße 2", "Germany", "", "", "", [], ""),
    ("pipetec-anlagenbau", "PipeTec Anlagenbau GmbH", "jsonld",
     "Leipzig", "04103", "Gerberstraße 41", "Germany",
     "+49 341 778 9900", "sales@pipetec-anlagenbau.de", "https://pipetec-anlagenbau.de",
     ["Pressure vessels", "Welding services", "Piping spools"],
     "ISO 9001:2015, ISO 14001, AD 2000, PED, ASME VIII"),
    ("nordwerk-schweisstechnik-hh", "Nordwerk Schweißtechnik GmbH", "plain",
     "Hamburg", "22761", "Ottenser Hauptstraße 14", "Germany",
     "+49 40 5566 7788", "info@nordwerk-schweisstechnik.de", "https://www.nordwerk-schweisstechnik.de",
     ["Welding services"], "ISO 9001"),
    ("alpenbau-schweisserei", "Alpenbau Schweißerei GmbH", "microdata",
     "München", "80331", "Sendlinger Straße 30", "Germany",
     "+49 89 223 4455", "office@alpenbau-schweisserei.de", "https://alpenbau-schweisserei.de",
     ["MIG/MAG welding", "Aluminium welding"], "ISO 9001, EN 1090-3"),
    ("baltic-weldtech", "Baltic WeldTech Sp. z o.o.", "jsonld",
     "Gdańsk", "80-180", "ul. Portowa 17", "Poland",
     "+48 58 555 1212", "biuro@balticweldtech.pl", "https://balticweldtech.pl",
     ["Offshore welding", "Subsea structures"], "ISO 9001:2015, ISO 3834-2, IATF 16949"),
    ("ferrum-industrieservice", "Ferrum Industrieservice GmbH", "plain",
     "Essen", "45127", "Rathenaustraße 9", "Germany",
     "+49 201 889 7766", "info@ferrum-is.de", "",
     ["Maintenance welding", "Turnaround services"], "ISO 45001, SCC**"),
    ("vulkan-apparatebau", "Vulkan Apparatebau AG", "microdata",
     "Mannheim", "68159", "Rheinvorlandstraße 3", "Germany",
     "+49 621 334 5566", "vertrieb@vulkan-apparatebau.de", "https://vulkan-apparatebau.de",
     ["Apparatus construction", "Heat exchangers", "Welding services"],
     "ISO 9001:2015, AD 2000, ASME U"),
]

PER_PAGE = 4
PAGES = (len(VENDORS) + PER_PAGE - 1) // PER_PAGE

ROBOTS = """User-agent: *
Crawl-delay: 0
Disallow: /company/blocked-vendor
Allow: /
"""


def card_html(v):
    slug, name, _, city = v[0], v[1], v[2], v[3]
    return f"""
      <article class="vendor-card" data-company-id="EP-{abs(hash(slug)) % 900000 + 100000}">
        <h2 class="vendor-name">{name}</h2>
        <span class="vendor-city">{city}</span>
        <a class="vendor-link" href="/company/{slug}">View supplier profile</a>
      </article>"""


def search_html(q, page):
    chunk = VENDORS[(page - 1) * PER_PAGE: page * PER_PAGE]
    cards = "".join(card_html(v) for v in chunk)
    # rel=next only on page 1 - forces the scraper to construct page 3's URL.
    nxt = (f'<a rel="next" class="pagination__next" href="/search?q={q}&page={page + 1}">Next</a>'
           if page == 1 and page < PAGES else "")
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{q} - suppliers, page {page}</title></head><body>
<h1>Search results for "{q}"</h1>
<section class="results">{cards}</section>
<nav class="pagination">{nxt}</nav>
</body></html>"""


def profile_html(v):
    (slug, name, style, city, postcode, street, country,
     phone, email, website, cats, certs) = v
    cat_items = "".join(f'<li><a href="/c/{re.sub(r"[^a-z]+", "-", c.lower())}">{c}</a></li>'
                        for c in cats)
    mail_html = f'<a href="mailto:{email}">{email}</a>' if email else "<span>Use contact form</span>"
    site_html = (f'<a class="company-website" rel="nofollow" href="{website}">{website}</a>'
                 if website else "")
    cert_html = f'<div class="certifications">{certs}</div>' if certs else ""

    head_extra = ""
    body_addr = f"""
      <address class="company-address">{street}, {postcode} {city}, {country}</address>"""

    if style == "jsonld":
        ld = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": name,
            "url": website or f"http://127.0.0.1/company/{slug}",
            "email": email,
            "telephone": phone,
            "identifier": f"EP-{abs(hash(slug)) % 900000 + 100000}",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": street,
                "addressLocality": city,
                "postalCode": postcode,
                "addressCountry": country,
            },
            "keywords": cats,
        }
        head_extra = (f'<script type="application/ld+json">{json.dumps(ld)}</script>')
    elif style == "microdata":
        body_addr = f"""
      <div itemscope itemtype="https://schema.org/Organization">
        <span itemprop="name">{name}</span>
        <span itemprop="telephone">{phone}</span>
        <span itemprop="email">{email}</span>
        <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
          <span itemprop="streetAddress">{street}</span>
          <span itemprop="postalCode">{postcode}</span>
          <span itemprop="addressLocality">{city}</span>
          <span itemprop="addressCountry">{country}</span>
        </div>
      </div>"""

    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{name}</title>{head_extra}</head><body data-company-id="EP-{abs(hash(slug)) % 900000 + 100000}">
  <h1 class="company-name">{name}</h1>
  {body_addr}
  <div class="contact">Tel: <a href="tel:{phone}">{phone}</a> | {mail_html}</div>
  {site_html}
  <ul class="categories">{cat_items}</ul>
  {cert_html}
  <a href="https://www.linkedin.com/company/{slug}">LinkedIn</a>
</body></html>"""


BY_SLUG = {v[0]: v for v in VENDORS}


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str, status: int = 200, ctype: str = "text/html; charset=utf-8"):
        raw = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):  # noqa: N802
        parts = urlsplit(self.path)
        path, qs = parts.path, parse_qs(parts.query)

        if path == "/robots.txt":
            return self._send(ROBOTS, ctype="text/plain; charset=utf-8")
        if path == "/jssearch":
            # Results injected client-side: invisible to requests, visible to Playwright.
            q = (qs.get("q") or ["welding"])[0]
            page = int((qs.get("page") or ["1"])[0])
            if page < 1 or page > PAGES:
                return self._send("<html><body><p>No results.</p></body></html>", 200)
            payload = json.dumps(search_html(q, page))
            return self._send(
                "<!doctype html><html><head><meta charset='utf-8'>"
                f"<title>{q} - js page {page}</title></head><body>"
                "<div id='app'></div><script>"
                f"const html = {payload};"
                "setTimeout(() => {"
                "  document.getElementById('app').innerHTML ="
                "    new DOMParser().parseFromString(html, 'text/html').body.innerHTML;"
                "}, 350);"
                "</script></body></html>")
        if path == "/search":
            q = (qs.get("q") or ["welding"])[0]
            page = int((qs.get("page") or ["1"])[0])
            if page < 1 or page > PAGES:
                return self._send("<html><body><p>No results.</p></body></html>", 200)
            return self._send(search_html(q, page))
        if path.startswith("/company/"):
            slug = path.rsplit("/", 1)[-1]
            if slug == "missing-page":
                return self._send("<html><body>Not found</body></html>", 404)
            v = BY_SLUG.get(slug)
            if not v:
                return self._send("<html><body>Not found</body></html>", 404)
            return self._send(profile_html(v))
        return self._send("<html><body>Not found</body></html>", 404)

    def log_message(self, fmt, *args):  # keep the scraper's log readable
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8099)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"mock directory on http://127.0.0.1:{args.port} ({len(VENDORS)} vendors, {PAGES} pages)")
    srv.serve_forever()
