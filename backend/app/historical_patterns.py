"""
A small, curated library of well-documented historical cases where a
news/macro event moved markets in a specific, explainable way.

These are for EDUCATIONAL CONTEXT ONLY - real, well-known past events,
described at a level of detail that's accurate and defensible, not
predictive rules. Markets don't repeat mechanically; the same type of
news can move prices differently depending on starting valuations,
positioning, and what investors already expected. Use these to
understand the *mechanism* (why a linkage exists), not to assume
history will replay the same way.
"""

HISTORICAL_PATTERNS = [
    {
        "id": "covid_2020_crash",
        "title": "COVID-19 crash & recovery, 2020",
        "period": "Feb-Apr 2020",
        "trigger": "Global lockdowns and demand collapse as COVID-19 spread worldwide.",
        "market_impact": (
            "Nifty 50 and Sensex fell roughly 35-38% peak-to-trough in about five weeks - one of the "
            "fastest crashes on record. Oil demand collapsed so sharply that US crude futures briefly "
            "traded negative in April 2020. Markets then recovered most losses within months, driven by "
            "central bank stimulus and vaccine-development news."
        ),
        "mechanism": (
            "Fear-driven, indiscriminate selling across almost every sector first (liquidity/panic phase), "
            "followed by a sharp, differentiated recovery favoring sectors seen as pandemic-resilient (IT, "
            "pharma) over those seen as most exposed (travel, hospitality, autos)."
        ),
        "sectors_most_affected": ["Aviation", "Hospitality", "Automobiles", "Banking"],
        "lesson": "Initial panic moves are often broad and emotional; the more informative, differentiated repricing happens in the weeks after as investors assess which businesses are actually impaired.",
    },
    {
        "id": "russia_ukraine_2022_oil_shock",
        "title": "Russia-Ukraine war & oil price shock, 2022",
        "period": "Feb-Jun 2022",
        "trigger": "Russia's invasion of Ukraine disrupted global energy supply expectations.",
        "market_impact": (
            "Brent crude spiked from around $95 to above $130/barrel within weeks. In India, this was a "
            "genuinely mixed picture, not a uniform 'market up' move: the broad Nifty/Sensex fell on "
            "inflation and import-bill worries, oil marketing companies (IOC, BPCL, HPCL) fell sharply on "
            "fears they'd have to absorb costs without raising retail fuel prices, while upstream names "
            "and Reliance's refining/O2C business saw margin tailwinds."
        ),
        "mechanism": (
            "A single commodity shock propagates differently depending on where a company sits in the "
            "value chain - producers/refiners can benefit while distributors/consumers with capped pricing "
            "power get squeezed, even within the same 'energy' sector."
        ),
        "sectors_most_affected": ["Oil Marketing (negative)", "Energy Upstream (positive)", "Aviation (negative)", "Broad market (negative, on inflation)"],
        "lesson": "This is the direct answer to 'does a Middle East war make Indian stocks rise' - it doesn't, in aggregate. India is a net oil importer; higher crude is a net headwind for the market even when it helps specific upstream stocks.",
    },
    {
        "id": "fed_taper_tantrum_2013",
        "title": "US Fed 'Taper Tantrum', 2013",
        "period": "May-Sep 2013",
        "trigger": "The US Federal Reserve signaled it would start reducing (tapering) its bond-buying stimulus.",
        "market_impact": (
            "The rupee fell sharply against the dollar (among the worst-hit emerging market currencies), "
            "FIIs pulled money out of Indian equities and bonds, and rate-sensitive sectors like banking, "
            "NBFCs, and real estate underperformed the broader market."
        ),
        "mechanism": (
            "Expectations of higher US yields make emerging-market assets relatively less attractive, "
            "triggering capital outflows; a weaker currency then adds imported inflation, prompting local "
            "central banks to consider rate hikes, which further pressures rate-sensitive sectors."
        ),
        "sectors_most_affected": ["Banking", "NBFC", "Real Estate"],
        "lesson": "US monetary policy signals move Indian markets even without any India-specific news - global rate expectations are a standing macro driver worth tracking on their own.",
    },
    {
        "id": "fed_hikes_2022_2023",
        "title": "US Fed rate-hike cycle, 2022-2023",
        "period": "Mar 2022-Jul 2023",
        "trigger": "The Fed raised interest rates aggressively to fight multi-decade-high US inflation.",
        "market_impact": (
            "Global tech/growth stocks (Nasdaq) underperformed on higher discount rates for future earnings "
            "and recession fears; Indian IT services stocks, which draw heavily on US tech-sector spending, "
            "underperformed the broader Indian market over the same period on fears of client budget cuts."
        ),
        "mechanism": (
            "Higher rates reduce the present value of far-out future profits, hitting growth/tech valuations "
            "hardest, and also raise recession odds in the client economy - a double drag on export-oriented "
            "sectors serving that economy."
        ),
        "sectors_most_affected": ["IT Services", "NBFC", "Real Estate"],
        "lesson": "A foreign central bank's decision can be one of the more reliable, trackable drivers for export-oriented sectors like Indian IT - which is why USD/INR and Nasdaq trends are tracked here as linked macro instruments.",
    },
    {
        "id": "demonetization_2016",
        "title": "India demonetization, 2016",
        "period": "Nov 2016-Q1 2017",
        "trigger": "The Indian government invalidated ₹500 and ₹1,000 notes overnight to curb black money.",
        "market_impact": (
            "Consumption-linked sectors (autos, FMCG, real estate) fell in the near term on a cash-liquidity "
            "crunch hitting informal-economy demand, while digital-payments-linked businesses saw a surge "
            "in usage and investor interest."
        ),
        "mechanism": (
            "A sudden domestic policy shock hit cash-dependent demand directly; markets initially priced in "
            "the disruption broadly before differentiating between cash-reliant and digital-native business "
            "models over subsequent quarters."
        ),
        "sectors_most_affected": ["Automobiles", "FMCG", "Real Estate"],
        "lesson": "Domestic policy shocks can matter as much as global ones, and again the market's first, broad reaction to a shock is usually followed by a more selective one as details emerge.",
    },
]


def get_all_patterns():
    return HISTORICAL_PATTERNS


def match_patterns_by_sector(sector: str):
    """Return historical cases whose 'sectors_most_affected' mentions this sector -
    used to surface relevant history next to a stock's current sector."""
    return [
        p for p in HISTORICAL_PATTERNS
        if any(sector.lower() in s.lower() for s in p["sectors_most_affected"])
    ]
