from typing import List

import requests

# Constants
COLUMNS = [
    "airport.iata",
    "airport.type",
    "city.name",
    "country.name",
]

PAGE_SIZE = 1000
LARGE_AIRPORT = "large_airport"

# API configuration
API_BASE_URL = "https://airportcodes.io/en/wp-json/aym/v1/table_data/airport/"
HEADERS = {
    "authority": "airportcodes.io",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cookie": "_ga=GA1.1.1776268612.1665360952; cookie_consent=%7B%22preferences%22%3Afalse%2C%22statistics%22%3Afalse%2C%22marketing%22%3Afalse%7D; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CPgocUAPgocUAEsABBENCkCgAAAAAH_AABpYAAAOhQD2F2K2kKEkfjSUWYAQBCujIEIhUAAAAECBIAAAAUgQAgFIIAgAAlACAAAAABAQAQCAgAQABAAAoACgAAAAAAAAAAAAAAQQAABAAIAAAAAAAAEAQAAIAAQAAAAAAABEhCAAQQAEAAAAAAAAAAAAAAAAAAABAAA%22%2C%221~%22%2C%228007520D-03DB-4FDD-B772-7BF2CD10B46E%22%5D%2Cnull%2Cnull%2C%5B%5D%5D; _ga_YTMNFT84BW=GS1.1.1665360952.1.1.1665361540.0.0.0",
    "referer": "https://airportcodes.io/en/all-airports/?filters[country]=FR",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}


def get_airport_codes(
    country_code: str, airport_type: str = LARGE_AIRPORT, page_size: int = PAGE_SIZE
) -> List[str]:
    """
    Fetch airport codes for a given country and airport type.
    """
    params = {
        "columns": ",".join(COLUMNS),
        "take": page_size,
        "skip": 0,
        "type": airport_type,
        "country": country_code,
    }
    response = requests.get(API_BASE_URL, headers=HEADERS, params=params)
    data = response.json()

    if data["status"] == "success":
        return [airport["airport.iata"] for airport in data["results"]]
    return []
