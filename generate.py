import json, os
from datetime import date

with open("data/hotels.json") as f:
    HOTELS = json.load(f)

SITE_NAME = "Kids Club Hotels"
BASE_URL = "https://kidsclubhotels.com"
TODAY = date.today().isoformat()

AREAS = sorted(set(h["area"] for h in HOTELS))
COUNTRIES = sorted(set(h["country"] for h in HOTELS))
ALL_TAGS = sorted(set(tag for h in HOTELS for tag in h["activity_tags"]))

def area_slug(a):
    return a.lower().replace(" ", "-").replace("(", "").replace(")", "")

def HEAD(title, desc, canonical, extra_schema="", prefix="."):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{prefix}/assets/style.css">
{extra_schema}
</head>
"""

def NAV(prefix="."):
    return f"""
<header class="site-header">
  <a href="{prefix}/index.html" class="logo">{SITE_NAME}</a>
  <nav>
    <a href="{prefix}/index.html">Search</a>
    <a href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">Seasonal closures guide</a>
    <a href="{prefix}/about.html">About</a>
    <a href="{prefix}/partner.html">Partner with Us</a>
  </nav>
</header>
"""

def FOOTER():
    return f"""
<footer class="site-footer">
  <p>{SITE_NAME} is an independent directory of family hotels with verified kids' clubs across Europe. We link to hotels' own booking pages where possible. Data on kids-club hours, staff languages, and seasonal closures is confirmed hotel-by-hotel as we build partnerships — fields marked "not yet confirmed" reflect that in-progress state, not a guess.</p>
  <p>&copy; {date.today().year} {SITE_NAME}</p>
</footer>
"""

os.makedirs("hotels", exist_ok=True)
os.makedirs("regions", exist_ok=True)
os.makedirs("articles", exist_ok=True)

# ---------- Individual hotel pages (prefix="..") ----------
for h in HOTELS:
    prefix = ".."
    url = f"{BASE_URL}/hotels/{h['slug']}.html"
    title = f"{h['name']} — Family Hotel with Kids' Club in {h['subregion']} | {SITE_NAME}"
    desc = f"{h['name']} in {h['subregion']}, {h['country']}: kids' club details, nearest airport ({h['airport']['primary']}), activities, and seasonal closure info."
    schema = {
        "@context": "https://schema.org",
        "@type": "Hotel",
        "name": h["name"],
        "address": {"@type": "PostalAddress", "addressRegion": h["subregion"], "addressCountry": h["country"]},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": t} for t in h["activity_tags"]],
        "url": url
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"Does {h['name']} have a kids' club?",
             "acceptedAnswer": {"@type": "Answer", "text": f"{h['name']} is a member of {h['brand']}, an association whose hotels are required to offer supervised childcare. Specific kids'-club ages and hours for this property are {h['kids_club']['ages'].lower()} — {SITE_NAME} confirms these details directly with each hotel as partnerships are finalized."}},
            {"@type": "Question", "name": f"What is the closest airport to {h['name']}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"The nearest major airport is {h['airport']['primary']}, with {h['airport']['alt']} as an alternative. {h['transport_note']}"}},
            {"@type": "Question", "name": f"When does {h['name']} close for the season?",
             "acceptedAnswer": {"@type": "Answer", "text": h["closure_note"]}},
        ]
    }
    html = HEAD(title, desc, url, f'<script type="application/ld+json">{json.dumps(schema)}</script>\n<script type="application/ld+json">{json.dumps(faq)}</script>', prefix=prefix) + f"""<body>
{NAV(prefix)}
<main class="hotel-profile">
  <p class="breadcrumb"><a href="{prefix}/index.html">Search</a> &rsaquo; <a href="{prefix}/regions/{area_slug(h['area'])}.html">{h['area']}</a> &rsaquo; {h['name']}</p>
  <h1>{h['name']}</h1>
  <p class="meta">{h['subregion']}, {h['country']} &middot; {h['brand']} &middot; Tier: {h['quality_tier']}</p>

  <section>
    <h2>Activities &amp; features</h2>
    <ul class="tag-list">
      {''.join(f'<li class="tag">{t}</li>' for t in h['activity_tags'])}
    </ul>
  </section>

  <section>
    <h2>Kids' club</h2>
    <table class="fact-table">
      <tr><th>Age range</th><td>{h['kids_club']['ages']}</td></tr>
      <tr><th>Hours</th><td>{h['kids_club']['hours']}</td></tr>
      <tr><th>Staff languages</th><td>{h['kids_club']['staff_languages']}</td></tr>
    </table>
    <p class="note">Status: {h['kids_club']['status']}. {SITE_NAME} verifies these fields directly with each hotel — see our <a href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">data verification notes</a>.</p>
  </section>

  <section>
    <h2>Getting there</h2>
    <table class="fact-table">
      <tr><th>Nearest airport</th><td>{h['airport']['primary']}</td></tr>
      <tr><th>Alternative airport</th><td>{h['airport']['alt']}</td></tr>
      <tr><th>Recommended transport</th><td>{h['transport_note']}</td></tr>
    </table>
  </section>

  <section>
    <h2>Seasonal closures</h2>
    <p>{h['closure_note']}</p>
  </section>

  <section>
    <h2>Book</h2>
    <p><a class="cta" href="{h['profile_source']}" rel="nofollow sponsored">View live rates &amp; book →</a></p>
    <p class="note">Booking route: {h['booking']['type']}.</p>
  </section>
</main>
{FOOTER()}
</body></html>"""
    with open(f"hotels/{h['slug']}.html", "w") as f:
        f.write(html)

# ---------- Region hub pages (prefix="..") ----------
for area in AREAS:
    prefix = ".."
    hotels_in_area = [h for h in HOTELS if h["area"] == area]
    url = f"{BASE_URL}/regions/{area_slug(area)}.html"
    title = f"Family Hotels with Kids' Clubs in {area} | {SITE_NAME}"
    desc = f"Browse {len(hotels_in_area)} verified family hotels with kids' clubs in {area}, with nearest airport, transport, and seasonal closure info for each."
    cards = "".join(f"""
      <article class="card">
        <h3><a href="{prefix}/hotels/{h['slug']}.html">{h['name']}</a></h3>
        <p>{h['subregion']}, {h['country']}</p>
        <ul class="tag-list">{''.join(f'<li class="tag">{t}</li>' for t in h['activity_tags'])}</ul>
        <p class="note">Nearest airport: {h['airport']['primary']}</p>
      </article>""" for h in hotels_in_area)
    html = HEAD(title, desc, url, prefix=prefix) + f"""<body>
{NAV(prefix)}
<main>
  <p class="breadcrumb"><a href="{prefix}/index.html">Search</a> &rsaquo; {area}</p>
  <h1>Family hotels with kids' clubs in {area}</h1>
  <p>{area} is home to {len(hotels_in_area)} hotels in our directory that belong to verified family-hotel associations (Kinderhotels Europa / Familienhotels Südtirol / Center Parcs Europe) and offer supervised kids' clubs. Use the filters on the <a href="{prefix}/index.html">search page</a> to narrow by activity or nearest airport.</p>
  <div class="card-grid">{cards}</div>
</main>
{FOOTER()}
</body></html>"""
    with open(f"regions/{area_slug(area)}.html", "w") as f:
        f.write(html)

# ---------- Homepage with search UI (prefix=".") ----------
prefix = "."
hotel_json = json.dumps(HOTELS)
areas_options = "".join(f'<option value="{a}">{a}</option>' for a in AREAS)
countries_options = "".join(f'<option value="{c}">{c}</option>' for c in COUNTRIES)
tag_checkboxes = "".join(f'<label class="checkbox"><input type="checkbox" name="activity" value="{t}"> {t}</label>' for t in ALL_TAGS)

itemlist_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        {"@type": "ListItem", "position": i+1, "url": f"{BASE_URL}/hotels/{h['slug']}.html", "name": h["name"]}
        for i, h in enumerate(HOTELS)
    ]
}

index_html = HEAD(
    f"Kids Club Hotels — Find Family Hotels with Real Kids' Clubs in Europe",
    "Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs. Search by location, nearest airport, English-speaking childcare, and activities like skiing or cycling.",
    f"{BASE_URL}/index.html",
    f'<script type="application/ld+json">{json.dumps(itemlist_schema)}</script>',
    prefix=prefix
) + f"""<body>
{NAV(prefix)}
<main>
  <h1>Find a family hotel with a real kids' club</h1>
  <p class="intro">Kids Club Hotels is an independent directory of {len(HOTELS)} European family hotels and resorts with verified kids' clubs — searchable by location, nearest airport, activities, and kids'-club language. Booking links go directly to each hotel's best available rate.</p>

  <form id="filters" class="filters">
    <div class="filter-group">
      <label for="area">Location</label>
      <select id="area" name="area">
        <option value="">All of Europe</option>
        {areas_options}
      </select>
    </div>
    <div class="filter-group">
      <label for="country">Country</label>
      <select id="country" name="country">
        <option value="">Any</option>
        {countries_options}
      </select>
    </div>
    <div class="filter-group">
      <label class="checkbox"><input type="checkbox" id="english-club"> Kids' club with English-speaking staff (confirmed only)</label>
    </div>
    <div class="filter-group">
      <fieldset>
        <legend>Activities</legend>
        {tag_checkboxes}
      </fieldset>
    </div>
  </form>

  <p id="result-count" class="note"></p>
  <div id="results" class="card-grid"></div>
</main>
{FOOTER()}

<script id="hotel-data" type="application/json">{hotel_json}</script>
<script src="{prefix}/assets/search.js"></script>
</body></html>"""

with open("index.html", "w") as f:
    f.write(index_html)

# ---------- About page (prefix=".") ----------
prefix = "."
about_html = HEAD(
    f"About | {SITE_NAME}",
    "Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs, built for parents who want real, confirmed information rather than marketing copy.",
    f"{BASE_URL}/about.html",
    prefix=prefix
) + f"""<body>
{NAV(prefix)}
<main class="static-page">
  <h1>About Kids Club Hotels</h1>
  <p>Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs. It exists for one reason: parents planning a family holiday need real, confirmed information — not marketing copy. Every hotel in this directory belongs to a recognised family-hotel association (Kinderhotels Europa, Familienhotels Südtirol, or Center Parcs Europe) and offers supervised childcare. We confirm the specifics — hours, age ranges, staff languages — directly with each property.</p>

  <h2>How we verify</h2>
  <p>Kids-club hours, age ranges, and staff languages are confirmed directly with hotel staff, not scraped from booking platforms or taken from brochure copy. Where a detail has not yet been confirmed with the property, we say so explicitly — fields marked "not yet confirmed" reflect that in-progress state, not a gap in our data. We update listings as confirmations come in and as seasonal operations change.</p>

  <h2>Contact</h2>
  <p>For hotel listings, corrections, or partnerships: <a href="mailto:hello@kidsclubhotels.com">hello@kidsclubhotels.com</a></p>
</main>
{FOOTER()}
</body></html>"""

with open("about.html", "w") as f:
    f.write(about_html)

# ---------- Partner with Us page (prefix=".") ----------
prefix = "."
partner_html = HEAD(
    f"Partner with Us | {SITE_NAME}",
    "Hotels with verified kids' clubs: list your property on Kids Club Hotels and earn qualified family bookings through a simple referral fee arrangement.",
    f"{BASE_URL}/partner.html",
    prefix=prefix
) + f"""<body>
{NAV(prefix)}
<main class="static-page">
  <h1>Partner with Kids Club Hotels</h1>
  <p>We list hotels with verified kids' clubs across Europe. If families find your hotel through our directory and book, we'd like to earn a small referral fee — here's how it works.</p>

  <h2>What we offer</h2>
  <ul>
    <li>A detailed, verified listing covering kids'-club hours, age ranges, staff languages, and activities</li>
    <li>Transport and nearest-airport information so families can plan their journey</li>
    <li>A direct booking link to your own website (not an OTA)</li>
    <li>Inclusion in our email newsletter and social content when relevant</li>
    <li>Priority placement in search results and regional guides for confirmed partners</li>
  </ul>

  <h2>What we ask</h2>
  <p>A referral fee of 5–8% on completed bookings that originate from Kids Club Hotels, or a flat monthly listing fee — we're flexible on structure depending on what works for your property. We prefer direct arrangements over routing through an OTA, which keeps the cost lower for both sides and keeps the booking relationship with you.</p>

  <h2>Get in touch</h2>
  <p>Email <a href="mailto:hello@kidsclubhotels.com">hello@kidsclubhotels.com</a> with your hotel name and a brief note about your kids' club. We'll follow up within 2 business days.</p>
</main>
{FOOTER()}
</body></html>"""

with open("partner.html", "w") as f:
    f.write(partner_html)

print("Generated:", len(HOTELS), "hotel pages,", len(AREAS), "region pages, 1 homepage, about.html, partner.html")
