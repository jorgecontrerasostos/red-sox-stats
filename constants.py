BATTING_URL = "https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?&env=prod&season=2025&sportId=1&stats=season&group=hitting&gameType=R&limit=25&offset=0&order=desc&teamId=111"
PITCHING_URL = "https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?&env=prod&season=2025&sportId=1&stats=season&group=pitching&gameType=R&limit=25&offset=0&&order=desc&teamId=111"

teams = {
    108: "Angels",
    109: "Diamondbacks",
    110: "Orioles",
    111: "Red Sox",
    112: "Cubs",
    113: "Reds",
    114: "Guardians",
    115: "Rockies",
    116: "Tigers",
    117: "Astros",
    118: "Royals",
    119: "Dodgers",
    120: "Nationals",
    121: "Mets",
    133: "Athletics",
    134: "Pirates",
    135: "Padres",
    136: "Mariners",
    137: "Giants",
    138: "Cardinals",
    139: "Rays",
    140: "Rangers",
    141: "Blue Jays",
    142: "Twins",
    143: "Philies",
    144: "Braves",
    145: "White Sox",
    146: "Marlins",
    147: "Yankees",
    158: "Brewers",
}

BATTING_HEADERS = {
    "accept": "*/*",
    "accept-language": "es-419,es;q=0.9,en;q=0.8",
    "origin": "https://www.mlb.com",
    "priority": "u=1, i",
    "referer": "https://www.mlb.com/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
}

PITCHING_HEADERS = {
    "sec-ch-ua-platform": '"Android"',
    "Referer": "https://www.mlb.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?1",
}

FLOAT_STATS = {"avg", "obp", "slg", "ops", "era", "whip", "k_per_9"}
