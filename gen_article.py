import json
from datetime import date

with open("data/hotels.json") as f:
    HOTELS = json.load(f)

SITE_NAME = "AlpineFamily"
BASE_URL = "https://example.com"
url = f"{BASE_URL}/articles/kids-club-hotel-closures-ski-season.html"
title = f"When Do Ski-Season Family Hotels Close? Kids'-Club Hotel Closure Dates | {SITE_NAME}"
desc = "Many Alpine family hotels with kids' clubs close for 1-3 weeks between winter and summer seasons. Here's why, and a hotel-by-hotel closure tracker."

faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Why do Alpine family hotels close between seasons?",
         "acceptedAnswer": {"@type": "Answer", "text": "Most independently owned Alpine hotels are family-run and use the low-demand weeks between ski season and summer season (typically mid-April to late May, and again in November) to renovate, give staff a break, and reset kids'-club programming for the next season. This is standard practice across the Kinderhotels Europa and Familienhotels Südtirol cooperatives, not a sign of a struggling property."}},
        {"@type": "Question", "name": "How do I find out if a specific family hotel is closed on my travel dates?",
         "acceptedAnswer": {"@type": "Answer", "text": "Check the hotel's own booking calendar directly, since closure windows shift year to year and by property. The table on this page tracks confirmed closure dates as we verify them hotel-by-hotel; entries marked \"not yet confirmed\" should be checked directly with the hotel before booking."}},
        {"@type": "Question", "name": "Does a hotel closure affect kids'-club availability specifically?",
         "acceptedAnswer": {"@type": "Answer", "text": "When a hotel is fully closed, the kids' club is closed too. Outside of full closures, some properties also run reduced kids'-club hours in shoulder-season weeks even while the hotel itself stays open — this is tracked separately from full closures where we have the data."}},
    ]
}

rows = "".join(
    f"<tr><td><a href='/hotels/{h['slug']}.html'>{h['name']}</a></td><td>{h['area']}</td><td>{h['closure_note']}</td></tr>"
    for h in HOTELS
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{json.dumps(faq)}</script>
</head>
<body>
<header class="site-header">
  <a href="/index.html" class="logo">{SITE_NAME}</a>
  <nav><a href="/index.html">Search</a><a href="/articles/kids-club-hotel-closures-ski-season.html">Seasonal closures guide</a></nav>
</header>
<main>
  <p class="breadcrumb"><a href="/index.html">Search</a> &rsaquo; Seasonal closures guide</p>
  <h1>When do ski-season family hotels close?</h1>
  <p class="intro">If you're booking a winter kids'-club hotel in the Alps, it's worth checking the hotel isn't in its off-season shutdown — a surprising number of small, family-run properties close for one to three weeks between the ski season and the summer season.</p>

  <h2>Why this happens</h2>
  <p>Most hotels in the Kinderhotels Europa and Familienhotels Südtirol cooperatives are independently owned and family-run, not corporate chains. The quiet weeks between ski season (usually ending mid-to-late April) and the start of summer bookings (late May/June) are when owners renovate rooms, give kids'-club and hospitality staff time off, and refresh the children's activity programming. A similar shorter closure often happens again in November between the end of summer/autumn hiking season and the start of ski season. This is routine for the industry — it isn't a sign of financial trouble at the property.</p>

  <h2>Hotel-by-hotel closure tracker</h2>
  <p>We confirm exact closure dates directly with each hotel as we build partnerships with them; until then, entries below are marked "not yet confirmed" rather than guessed. Always double-check directly with the hotel for your specific travel dates.</p>
  <table class="compare">
    <tr><th>Hotel</th><th>Area</th><th>Closure status</th></tr>
    {rows}
  </table>

  <h2>What to do if you're booking during a shoulder season</h2>
  <p>Call or email the hotel directly to confirm both (a) whether the property itself is open on your dates, and (b) whether the kids' club is running full hours — some hotels stay open with reduced childcare staffing in the lowest-demand weeks even without a full closure.</p>
</main>
<footer class="site-footer">
  <p>{SITE_NAME} is an independent directory of family hotels with verified kids' clubs across Europe.</p>
  <p>&copy; {date.today().year} {SITE_NAME}</p>
</footer>
</body>
</html>"""

with open("articles/kids-club-hotel-closures-ski-season.html", "w") as f:
    f.write(html)
print("Article written")
