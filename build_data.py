import re
import json

import unicodedata
def slug(s):
    s = s.replace("&", "and").replace("+", "and")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s

AIRPORTS = {
    "Austrian Alps": {"primary": "Innsbruck (INN)", "alt": "Munich (MUC)"},
    "Austrian Alps (Salzburg)": {"primary": "Salzburg (SZG)", "alt": "Munich (MUC)"},
    "Austrian Alps (Styria)": {"primary": "Graz (GRZ)", "alt": "Salzburg (SZG)"},
    "Austrian Lakes": {"primary": "Klagenfurt (KLU)", "alt": "Salzburg (SZG) / Vienna (VIE)"},
    "Dolomites (South Tyrol)": {"primary": "Bolzano (BZO)", "alt": "Innsbruck (INN) / Verona (VRN)"},
    "Italian Alps (Trentino)": {"primary": "Verona (VRN)", "alt": "Bergamo (BGY)"},
    "Adriatic Coast (Italy)": {"primary": "Venice (VCE)", "alt": "Trieste (TRS)"},
}

TRANSPORT_NOTES = {
    "Austrian Alps": "Regional rail (ÖBB) reaches the main valley towns; most ski villages need a connecting shuttle, taxi or hotel transfer for the final stretch. A rental car gives the most flexibility for ski luggage.",
    "Austrian Alps (Salzburg)": "Regional rail to the valley hub, then hotel shuttle/taxi for the final leg. Many Kinderhotels properties offer an airport/train transfer directly (see amenities).",
    "Austrian Alps (Styria)": "Regional rail to Irdning-Donnersbachtal or similar hub, then short taxi/shuttle. A car is the easier option for this area.",
    "Austrian Lakes": "Direct regional rail service reaches most lake towns in Carinthia; a car is useful for the more remote lakeside properties, especially outside summer.",
    "Dolomites (South Tyrol)": "High-speed rail to Bolzano/Bressanone, then a regional bus or hotel transfer into the valleys — many Dolomite villages sit off the rail line, so budget 45-90 minutes for the connection.",
    "Italian Alps (Trentino)": "Rail to Trento or Rovereto, then bus/transfer into the Ledro valley. A car is more flexible given limited bus frequency.",
    "Adriatic Coast (Italy)": "Direct rail or highway link from Venice; a car is worth having in peak summer for coastal-town congestion.",
}

def hotel(name, country, region_area, subregion, tier, tags, note=""):
    return {
        "name": name,
        "slug": slug(name),
        "brand": "Kinderhotels Europa",
        "country": country,
        "area": region_area,
        "subregion": subregion,
        "quality_tier": tier,
        "activity_tags": tags,
        "airport": AIRPORTS.get(region_area, {"primary": "TBD", "alt": "TBD"}),
        "transport_note": TRANSPORT_NOTES.get(region_area, "TBD"),
        "kids_club": {
            "ages": "Not yet confirmed",
            "hours": "Not yet confirmed",
            "staff_languages": "Not yet confirmed",
            "status": "unconfirmed"
        },
        "closure_note": "Not yet confirmed with hotel. Many Alpine family hotels close for 1-3 weeks between the winter and summer seasons (typically mid-April and again in November) — always confirm exact dates before booking.",
        "profile_source": "https://www.kinderhotels.com/en/hotels/",
        "booking": {"type": "OTA affiliate (pending direct deal)", "note": note}
    }

HOTELS = [
    hotel("Kinderhotel Kröller","Austria","Austrian Alps","Gerlos, Tyrol","Premium",["Skiing","Baby-focused"]),
    hotel("Pitzis Kinderhotel","Austria","Austrian Alps","Arzl im Pitztal, Tyrol","Premium",["Baby-focused","Airport/train transfer"]),
    hotel("Family & Sports Resort Brennseehof","Austria","Austrian Lakes","Feld am See, Carinthia","Premium",["Lake","Sports"]),
    hotel("Heidi-Hotel Falkertsee","Austria","Austrian Lakes","Falkert / Bad Kleinkirchheim, Carinthia","Premium",["Skiing","Pets allowed"]),
    hotel("Family Hotel Kreuzwirt","Austria","Austrian Lakes","Weissensee, Carinthia","Premium",["Lake","Cycling"]),
    hotel("Ferienwelt Kesselgrub","Austria","Austrian Alps (Salzburg)","Altenmarkt-Zauchensee, Salzburg","Premium",["Baby-focused","Barrier-free"]),
    hotel("Garberhof Dolomit Family","Italy","Dolomites (South Tyrol)","Rasen-Antholz","Premium",["Pets allowed","Cycling"]),
    hotel("Imperial Aparthotel","Italy","Adriatic Coast (Italy)","Bibione, Veneto","Premium",["Beach","Aparthotel"]),
    hotel("Familienresort Buchau","Austria","Austrian Alps","Eben am Achensee, Tyrol","Premium Plus",["Lake","Baby-focused"]),
    hotel("Almhof Family Resort & SPA","Austria","Austrian Alps","Gerlos, Tyrol","Premium Plus",["Skiing","Spa"]),
    hotel("Smiley's Kinderhotel","Austria","Austrian Lakes","Trebesing / Katschberg, Carinthia","Premium",["Lake","Airport/train transfer"]),
    hotel("Kinderhotel Stegerhof","Austria","Austrian Alps (Styria)","Donnersbachwald, Styria","Premium",["Skiing","Cycling"]),
    hotel("Family Hotel Adriana","Italy","Italian Alps (Trentino)","Ledro, Trentino","Premium",["Baby-focused","Equipment rental"]),
    hotel("Kinderhotel Felben","Austria","Austrian Alps (Salzburg)","Mittersill, Salzburg","Premium",["Baby-focused","Cycling"]),
    hotel("Baby & Kinder Hotel Laurentius","Austria","Austrian Alps","Fiss, Tyrol","Premium Plus",["Skiing","Baby-focused"]),
    hotel("Baby + Kinder Hotel Sonnelino","Austria","Austrian Lakes","St. Kanzian (Lake Klopeiner See), Carinthia","Premium",["Lake","Cycling"]),
    hotel("Familienparadies Sporthotel Achensee","Austria","Austrian Alps","Achenkirch, Tyrol","Premium",["Skiing","Lake"]),
    hotel("Kinderhotel Alpenresidenz Ballunspitze","Austria","Austrian Alps","Galtür, Tyrol","Premium",["Baby-focused","Pets allowed"]),
    hotel("Adventure Family Hotel Maria & Lodge","Italy","Dolomites (South Tyrol)","Obereggen","Premium",["Skiing","Cycling"]),
    hotel("Kinderhotel Laderhof","Austria","Austrian Alps","Ladis, Tyrol","Premium",["Baby-focused"]),
    hotel("ELLMAUHOF - the Generations Resort","Austria","Austrian Alps (Salzburg)","Saalbach Hinterglemm, Salzburg","Premium Plus",["Skiing","Multigenerational"]),
    hotel("Leading Family Hotels Löwe and Bär","Austria","Austrian Alps","Serfaus, Tyrol","Premium Plus",["Skiing","Family suites"]),
    hotel("Familienhotel Post am Millstätter See","Austria","Austrian Lakes","Millstatt am See, Carinthia","Premium",["Lake"]),
    {**hotel("Falkensteiner Family Resort Lido","Italy","Dolomites (South Tyrol)","Ehrenburg, Pustertal","N/A",["Larger resort"]),"brand":"Familienhotels Südtirol","booking":{"type":"OTA affiliate (verify membership)","note":"Verify current association membership before outreach"}},
    {**hotel("Das Mühlwald Quality Time Family Resort","Italy","Dolomites (South Tyrol)","Natz, Pustertal","N/A",["Larger resort"]),"brand":"Familienhotels Südtirol","booking":{"type":"OTA affiliate (verify membership)","note":"Verify current association membership before outreach"}},
    {**hotel("Feuerstein Nature Family Resort","Italy","Dolomites (South Tyrol)","South Tyrol","N/A",["Montessori-based childcare, 70 hrs/week"]),"brand":"Familienhotels Südtirol","booking":{"type":"OTA affiliate (verify membership)","note":"Verify current association membership before outreach"}},
]

with open("data/hotels.json","w") as f:
    json.dump(HOTELS, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(HOTELS)} hotels")
