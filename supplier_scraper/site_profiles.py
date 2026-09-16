"""Per-directory selector profiles.

A profile is just a bag of CSS selector *candidates*. The extractor tries each
candidate in order and keeps the first non-empty hit, so a profile degrades
gracefully when a site reshuffles its markup: the JSON-LD / microdata /
mailto-tel fallbacks in scraper.py still fill most fields.

IMPORTANT
---------
The europages / wlw selectors below are best-known patterns, not selectors
verified against the live DOM (see README - this project was built in a
sandbox whose egress policy blocks those hosts). Run

    python scraper.py --inspect

once against your target domain: it prints the real container/card/pagination
structure of the search page plus the candidate field blocks of one profile
page, which is everything you need to correct the lists below.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SiteProfile:
    name: str
    domains: tuple
    # {keyword} is URL-quoted, {page} is the 1-based page number.
    search_url_template: str
    engine: str = "auto"

    # --- search results page -------------------------------------------------
    result_card: List[str] = field(default_factory=list)
    profile_link: List[str] = field(default_factory=list)
    next_page: List[str] = field(default_factory=list)
    card_name: List[str] = field(default_factory=list)
    card_city: List[str] = field(default_factory=list)

    # --- company profile page ------------------------------------------------
    p_name: List[str] = field(default_factory=list)
    p_website: List[str] = field(default_factory=list)
    p_email: List[str] = field(default_factory=list)
    p_phone: List[str] = field(default_factory=list)
    p_address: List[str] = field(default_factory=list)
    p_city: List[str] = field(default_factory=list)
    p_postal_code: List[str] = field(default_factory=list)
    p_country: List[str] = field(default_factory=list)
    p_categories: List[str] = field(default_factory=list)
    p_certifications: List[str] = field(default_factory=list)
    # Attribute on the card or profile root that carries the directory's own id.
    p_internal_id: List[str] = field(default_factory=list)

    def build_search_url(self, keyword_quoted: str, page: int) -> str:
        return self.search_url_template.format(keyword=keyword_quoted, page=page)


# Selectors shared by most B2B directories; every profile inherits them as a
# tail so the generic heuristics always get a chance.
_COMMON_CARD = [
    "article", "li[data-company]", "div[data-company-id]",
    "div.company-card", "div.result-item", "li.search-result",
]
_COMMON_LINK = [
    "a[href*='/company']", "a[href*='/unternehmen']", "a[href*='/azienda']",
    "a[href*='/firma']", "a[href*='/profil']", "h2 a", "h3 a", "a",
]
_COMMON_NEXT = [
    "a[rel='next']", "link[rel='next']", "a.next", "a.pagination__next",
    "a[aria-label*='ext']", "li.next > a", "a[data-testid='pagination-next']",
]

EUROPAGES = SiteProfile(
    name="europages",
    domains=(
        "europages.co.uk", "europages.de", "europages.it", "europages.fr",
        "europages.es", "europages.nl", "europages.pl", "www.europages.co.uk",
        "www.europages.de", "www.europages.it",
    ),
    # Europages paginates as .../companies/<page>/<keyword>.html
    search_url_template="https://{domain}/companies/{page}/{keyword}.html",
    engine="auto",
    result_card=["div.ep-result-card", "article.ep-company", "li.search-item"] + _COMMON_CARD,
    profile_link=["a.ep-company__link", "a[href*='/firmen/']", "a[href*='/companies/']"] + _COMMON_LINK,
    next_page=["a.pagination-next", "a[data-test='pagination-next']"] + _COMMON_NEXT,
    card_name=["h2", "h3", ".ep-company__name"],
    card_city=[".ep-company__city", ".company-city", "span[class*='city']"],
    p_name=["h1", "[itemprop='name']", "meta[property='og:title']"],
    p_website=[
        "a[data-test='company-website']", "a[rel='nofollow'][href^='http']",
        "a[itemprop='url']", "a[href^='http']:-soup-contains('www.')",
    ],
    p_email=["a[href^='mailto:']", "[itemprop='email']"],
    p_phone=["a[href^='tel:']", "[itemprop='telephone']", "[data-test='company-phone']"],
    p_address=["[itemprop='address']", "address", ".company-address", "[class*='address']"],
    p_city=["[itemprop='addressLocality']"],
    p_postal_code=["[itemprop='postalCode']"],
    p_country=["[itemprop='addressCountry']", ".company-country"],
    p_categories=[
        "a[href*='/business-directory']", ".company-activities a",
        "[class*='categor'] a", "[class*='activit'] a", "ul.keywords a",
    ],
    p_certifications=["[class*='certif']", "[class*='label']", "[class*='badge']"],
    p_internal_id=["[data-company-id]", "[data-epid]", "[data-id]"],
)

WLW = SiteProfile(
    name="wlw",
    domains=("wlw.de", "www.wlw.de", "wlw.at", "wlw.ch"),
    search_url_template="https://{domain}/de/suche?q={keyword}&page={page}",
    engine="playwright",  # wlw renders results client-side
    result_card=["article[data-testid='supplier-card']", "div[data-testid='result-card']"] + _COMMON_CARD,
    profile_link=["a[href*='/de/firma/']", "a[data-testid='supplier-link']"] + _COMMON_LINK,
    next_page=["a[data-testid='pagination-next']", "button[aria-label*='eiter']"] + _COMMON_NEXT,
    card_name=["h2", "h3", "[data-testid='supplier-name']"],
    card_city=["[data-testid='supplier-location']", "span[class*='location']"],
    p_name=["h1", "[itemprop='name']"],
    p_website=["a[data-testid='company-website']", "a[rel='nofollow'][href^='http']"],
    p_email=["a[href^='mailto:']", "[itemprop='email']"],
    p_phone=["a[href^='tel:']", "[itemprop='telephone']"],
    p_address=["address", "[itemprop='address']", "[class*='address']"],
    p_city=["[itemprop='addressLocality']"],
    p_postal_code=["[itemprop='postalCode']"],
    p_country=["[itemprop='addressCountry']"],
    p_categories=["[data-testid='category'] a", "[class*='categor'] a", "ul.keywords a"],
    p_certifications=["[class*='certif']", "[class*='zertifi']", "[class*='badge']"],
    p_internal_id=["[data-supplier-id]", "[data-company-id]", "[data-id]"],
)

GENERIC = SiteProfile(
    name="generic",
    domains=(),
    search_url_template="https://{domain}/search?q={keyword}&page={page}",
    engine="auto",
    result_card=["article.vendor-card"] + _COMMON_CARD,
    profile_link=["a.vendor-link"] + _COMMON_LINK,
    next_page=_COMMON_NEXT,
    card_name=["h2", "h3", "[class*='name']"],
    card_city=["[class*='city']", "[class*='location']"],
    p_name=["h1", "[itemprop='name']", "meta[property='og:title']"],
    p_website=["a[href^='http'][rel='nofollow']", "a[itemprop='url']", "a[class*='website']"],
    p_email=["a[href^='mailto:']", "[itemprop='email']", "[class*='email']"],
    p_phone=["a[href^='tel:']", "[itemprop='telephone']", "[class*='phone']"],
    p_address=["[itemprop='address']", "address", "[class*='address']"],
    p_city=["[itemprop='addressLocality']", "[class*='city']"],
    p_postal_code=["[itemprop='postalCode']", "[class*='postal']", "[class*='zip']"],
    p_country=["[itemprop='addressCountry']", "[class*='country']"],
    p_categories=["[class*='categor'] a", "[class*='service'] a", "ul.keywords a", "[class*='categor'] li"],
    p_certifications=["[class*='certif']", "[class*='standard']", "[class*='badge']"],
    p_internal_id=["[data-company-id]", "[data-vendor-id]", "[data-id]"],
)

ALL_PROFILES = (EUROPAGES, WLW, GENERIC)


def profile_for(domain: str) -> SiteProfile:
    """Pick the profile whose domain list matches, else the generic one."""
    host = domain.lower().split("/")[0]
    bare = host.split(":")[0]
    for prof in ALL_PROFILES:
        if bare in prof.domains or host in prof.domains:
            return prof
        for known in prof.domains:
            if bare.endswith("." + known) or bare == known:
                return prof
    return GENERIC
