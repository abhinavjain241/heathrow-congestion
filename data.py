from typing import Dict, List, Tuple

# Data
eligible_countries: Dict[str, str] = {
    "Australia": "AU",
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Canada": "CA",
    "Croatia": "HR",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Iceland": "IS",
    "Ireland": "IE",
    "Italy": "IT",
    "Japan": "JP",
    "Latvia": "LV",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Malta": "MT",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Norway": "NO",
    "Poland": "PL",
    "Portugal": "PT",
    "Republic of Cyprus": "CY",
    "Romania": "RO",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "South Korea": "KR",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "UK": "GB",
    "USA": "US",
}

# Store as min and max passengers for given plane type
plane_types: Dict[str, Tuple[int, int]] = {
    "Boeing 777-200 / 200ER Passenger": (301, 440),
    "Airbus A330-300 Passenger": (250, 440),
    "Boeing 767-400 Passenger": (245, 375),
    "Boeing 787-10": (330, 440),
    "Airbus A318 Passenger": (107, 132),
    "Boeing 767-300 Passenger (winglets)": (210, 350),
    "Airbus A330-200 Passenger": (210, 406),
    "Airbus A320neo": (150, 180),
    "Airbus A321 Passenger (sharklets)": (185, 236),
    "Boeing 767-300 Passenger": (210, 350),
    "Airbus A220-300 Passenger": (120, 160),
    "Boeing 787-8": (242, 359),
    "Boeing 737 MAX 8": (162, 210),
    "Airbus A350-1000": (350, 410),
    "Airbus A220-100 Passenger": (100, 135),
    "Airbus A321neo": (180, 240),
    "Boeing 777 Passenger": (301, 550),
    "Boeing 787": (242, 440),
    "Boeing 777-300ER Passenger": (350, 550),
    "Airbus A321 Passenger": (185, 236),
    "Airbus A319 Passenger": (124, 156),
    "Airbus A320 Passenger (sharklets)": (150, 180),
    "Airbus A320 Passenger": (150, 180),
    "Boeing 777-200LR Passenger": (301, 440),
    "Airbus A350": (300, 410),
    "Boeing 777-300 Passenger": (368, 550),
    "Boeing 787-9": (290, 420),
    "Boeing 737-700 Passenger/BBJ1 (winglets)": (126, 149),
    "Airbus A380-800 Passenger": (400, 850),
    "Airbus A350-900": (300, 350),
    "Boeing 747-8 Passenger": (410, 605),
    "Airbus A330-900neo Passenger": (260, 440),
    "Boeing 737-800 Passenger/BBJ2 (winglets)": (162, 189),
    "Airbus A330 Passenger": (210, 440),
}

country_airport_codes: Dict[str, List[str]] = {
    "AU": ["ADL", "BNE", "CBR", "MEL", "PER", "SYD"],
    "AT": ["VIE"],
    "BE": ["BRU", "CRL", "LGG"],
    "BG": ["BOJ", "SOF", "VAR"],
    "CA": ["YYC", "YEG", "YHZ", "YYZ", "YUL", "YOW", "YYT", "YVR", "YYJ", "YWG"],
    "HR": ["ZAG"],
    "CZ": ["PRG"],
    "DK": ["AAL", "BLL", "CPH"],
    "EE": ["TLL"],
    "FI": ["HEL"],
    "FR": ["BOD", "CDG", "BSL", "LYS", "MRS", "NCE", "ORY", "TLS"],
    "DE": [
        "SXF",
        "TXL",
        "BRE",
        "CGN",
        "DTM",
        "DRS",
        "DUS",
        "FRA",
        "HAM",
        "HAJ",
        "FKB",
        "LEJ",
        "MUC",
        "FMO",
        "NUE",
        "RMS",
        "STR",
        "BER",
    ],
    "GR": ["ATH", "HER", "SKG"],
    "HU": ["BUD"],
    "IS": ["KEF"],
    "IE": ["ORK", "DUB", "SNN"],
    "IT": [
        "BRI",
        "BLQ",
        "CAG",
        "CTA",
        "CIA",
        "PMO",
        "GOA",
        "BGY",
        "FCO",
        "MXP",
        "LIN",
        "NAP",
        "PSA",
        "TSF",
        "TRN",
        "VCE",
        "VRN",
    ],
    "JP": [
        "NGO",
        "FUK",
        "DNA",
        "KOJ",
        "KIX",
        "FSZ",
        "OKA",
        "NRT",
        "CTS",
        "ITM",
        "HND",
        "OKO",
    ],
    "LV": ["RIX"],
    "LI": [],
    "LT": ["VNO"],
    "LU": ["LUX"],
    "MT": ["MLA"],
    "NL": ["AMS", "EIN"],
    "NZ": ["AKL", "CHC", "WLG"],
    "NO": ["BGO", "BOO", "OSL", "SVG", "TOS", "TRD"],
    "PL": ["WRO", "GDN", "KTW", "KRK", "WMI", "POZ", "WAW"],
    "PT": ["FAO", "OPO", "LIS", "PDL", "TER"],
    "CY": ["LCA", "PFO"],
    "RO": ["OTP"],
    "SG": ["SIN"],
    "SK": ["BTS"],
    "SI": ["LJU"],
    "KR": ["PUS", "GMP", "ICN", "CJU", "KUV", "MWX", "OSN"],
    "ES": ["MAD", "ALC", "BCN", "LPA", "SPC", "AGP", "PMI", "SCQ", "TFN", "TFS", "IBZ"],
    "SE": ["GOT", "LLA", "MMX", "ARN"],
    "CH": ["GVA", "ZRH"],
    "GB": [
        "ABZ",
        "BFS",
        "BHX",
        "BOH",
        "BRS",
        "CWL",
        "EMA",
        "EDI",
        "EXT",
        "BHD",
        "GLA",
        "LBA",
        "LPL",
        "LGW",
        "LHR",
        "LTN",
        "STN",
        "MAN",
        "NCL",
        "NWI",
        "AKT",
        "BZZ",
        "FFD",
        "LKZ",
        "MHZ",
        "DSA",
        "SOU",
    ],
    "US": [
        "SPI",
        "ABQ",
        "LTS",
        "AVL",
        "AGS",
        "AUS",
        "GRB",
        "BWI",
        "BGR",
        "BAD",
        "BAB",
        "LIT",
        "BIL",
        "BHM",
        "LEX",
        "BFI",
        "BOI",
        "BDL",
        "BUF",
        "CVS",
        "BMI",
        "CHS",
        "CLT",
        "MDW",
        "ORD",
        "RFD",
        "CVG",
        "COS",
        "CLE",
        "CAE",
        "CBM",
        "CRP",
        "DFW",
        "DAL",
        "MSN",
        "HNL",
        "DAB",
        "DEN",
        "DSM",
        "VPS",
        "DTW",
        "DLF",
        "MGE",
        "DOV",
        "DBQ",
        "DLH",
        "DYS",
        "EDW",
        "OMA",
        "ERI",
        "FAI",
        "SKA",
        "FLL",
        "FSM",
        "FWA",
        "AFW",
        "FTW",
        "BOS",
        "MKE",
        "PIA",
        "IAH",
        "ROC",
        "GSP",
        "GUS",
        "GPT",
        "ATL",
        "HMN",
        "HSV",
        "IND",
        "JAN",
        "JAX",
        "DAY",
        "JFK",
        "CMH",
        "SNA",
        "ADW",
        "JLN",
        "MCI",
        "LGA",
        "LFT",
        "LFI",
        "LAX",
        "MSY",
        "SDF",
        "CHA",
        "LBB",
        "LUF",
        "MCF",
        "MHT",
        "MBS",
        "LAS",
        "TCM",
        "TYS",
        "MEM",
        "OAK",
        "MIA",
        "MSP",
        "MOB",
        "MLU",
        "MGM",
        "MUO",
        "BNA",
        "EWR",
        "PHF",
        "ORF",
        "SJC",
        "ONT",
        "MCO",
        "SFB",
        "PBI",
        "PHL",
        "PHX",
        "GSO",
        "PIT",
        "PDX",
        "PWM",
        "MLI",
        "RDU",
        "RND",
        "HIB",
        "RNO",
        "RIC",
        "AMA",
        "LCK",
        "ROA",
        "WRB",
        "RST",
        "DCA",
        "SMF",
        "SLC",
        "SAT",
        "SAN",
        "SFO",
        "SRQ",
        "SAV",
        "BLV",
        "SEA",
        "GSB",
        "SSC",
        "SPS",
        "SUX",
        "SBN",
        "RSW",
        "SUS",
        "GEG",
        "SGF",
        "STL",
        "SYR",
        "TLH",
        "TPA",
        "ANC",
        "CID",
        "PVD",
        "TIK",
        "TOL",
        "SUU",
        "TRI",
        "HTS",
        "TUS",
        "TUL",
        "PAM",
        "END",
        "VBG",
        "IAD",
        "SZL",
        "ICT",
        "OKC",
        "HOU",
        "FFO",
        "CRW",
    ],
}


def get_all_privileged_airports() -> List[str]:
    """
    Get a list of all privileged airports from country_airport_codes.
    """
    return [
        airport for airports in country_airport_codes.values() for airport in airports
    ]
