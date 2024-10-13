import json
from datetime import datetime, timedelta
from enum import Enum
from functools import cache
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd
import requests

from api_types import (AirportFacility, FlightResponse, FlightServiceResponse,
                       PortOfCall)
from data import get_all_privileged_airports, plane_types

headers = {
    "authority": "api-dp-prod.dp.heathrow.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cookie": "CONSENTMGR=consent:true%7Cts:1664550363206; _gcl_au=1.1.831568864.1664550370; _fbp=fb.1.1664550370469.1713077638; _cs_c=0; AMCVS_FCD067055294DE7D0A490D44%40AdobeOrg=1; AMCV_FCD067055294DE7D0A490D44%40AdobeOrg=1585540135%7CMCIDTS%7C19275%7CMCMID%7C84066851465478410963587924572127353985%7CMCAAMLH-1665927283%7C6%7CMCAAMB-1665927283%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1665329683s%7CNONE%7CvVersion%7C4.4.0; check=true; _cs_mk=0.4516726686286334_1665322483804; s_cc=true; _cs_cvars=%7B%221%22%3A%5B%22Page%20ID%22%2C%22%2Fcontent%2Fheathrow%2Fmain%2Fgb%2Fen%2Farrivals%22%5D%2C%222%22%3A%5B%22Language%22%2C%22en-GB%22%5D%2C%223%22%3A%5B%22Breadcrumb%22%2C%22Heathrow%3A%20Welcome%20to%20Heathrow%20Airport%22%5D%2C%224%22%3A%5B%22PageName%22%2C%22en%20%7C%20heathrowairport%20%7C%20en%20%7C%20arrivals%22%5D%7D; mbox=PC#e85b48f8536740f299ea70f867e04f00.37_0#1728567303|session#d293fff3433b46069ad49f77cca2300d#1665324344; utag_main=v_id:01838eeed8c800b02ea7788f0b7805075002106d00b7e$_sn:2$_se:2$_ss:0$_st:1665324302134$dc_visit:2$ses_id:1665322483590%3Bexp-session$_pn:2%3Bexp-session$dc_event:2%3Bexp-session$dc_region:eu-west-1%3Bexp-session; _cs_id=ad4d8dcd-d17c-ae8f-d721-b28b29c3858f.1664550374.2.1665322502.1665322485.1617038729.1698714374385; _cs_s=2.5.0.1665324302915; s_sq=baalhrprod%252Cbaalhrglobal%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fwww.heathrow.com%25252Farrivals%2526link%253D19%2526region%253Dflight-list-app%2526.activitymap%2526.a%2526.c",
    "origin": "https://www.heathrow.com",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}


class PortOfCallType(Enum):
    ORIGIN = "ORIGIN"
    DESTINATION = "DESTINATION"


def get_port_of_call(portsOfCall: list, type: PortOfCallType):
    return next(
        (
            portOfCall
            for portOfCall in portsOfCall
            if portOfCall["portOfCallType"] == type.value
        ),
        None,
    )


def get_airport(portOfCall: PortOfCall) -> tuple[str, str]:
    airportFacility: AirportFacility = portOfCall["airportFacility"]
    airport_id = airportFacility.get("iataIdentifier", "")
    airport_city = airportFacility["airportCityLocation"].get("name", "")
    return airport_id, airport_city


def get_scheduled_time(portOfCall: PortOfCall):
    if "operatingTimes" in portOfCall and "scheduled" in portOfCall["operatingTimes"]:
        return portOfCall["operatingTimes"]["scheduled"]["local"]
    return None


def get_plane_type(flight_service: FlightServiceResponse) -> str:
    if (
        "aircraftTransport" not in flight_service
        or "description" not in flight_service["aircraftTransport"]
    ):
        return ""
    return flight_service["aircraftTransport"]["description"]


def get_flight_carrier(flight_service: FlightServiceResponse) -> str:
    if (
        "airlineParty" not in flight_service
        or "name" not in flight_service["airlineParty"]
    ):
        return ""
    return flight_service["airlineParty"]["name"]


def estimate_passengers(plane_type: str) -> int:
    if plane_type in plane_types:
        min_capacity, max_capacity = plane_types[plane_type]
        return (min_capacity + max_capacity) // 2  # Use average capacity
    return 200  # Default estimate if plane type is unknown


def parse_response(response: list[FlightResponse]):
    flight_infos = []
    for flight in response:
        flight_service: FlightServiceResponse = flight["flightService"]
        aircraftMovement = flight_service["aircraftMovement"]
        if aircraftMovement is not None and "route" in aircraftMovement:
            route = aircraftMovement["route"]
            if route is not None and "portsOfCall" in route:
                portsOfCall = route["portsOfCall"]
                origin = get_port_of_call(portsOfCall, PortOfCallType.ORIGIN)
                destination = get_port_of_call(portsOfCall, PortOfCallType.DESTINATION)
                origin_airport, origin_city = get_airport(origin)
                arrival_time = get_scheduled_time(destination)  # Arrival in LHR
                plane_type = get_plane_type(flight_service)
                estimated_passengers = estimate_passengers(plane_type)
                flight_infos.append(
                    {
                        "flightNumber": flight_service["iataFlightIdentifier"],
                        "flightCarrier": get_flight_carrier(flight_service),
                        "planeType": plane_type,
                        "origin_airport": origin_airport,
                        "origin_city": origin_city,
                        "arrival_time": arrival_time,
                        "estimated_passengers": estimated_passengers,
                    }
                )
    return flight_infos


@cache
def get_arrivals(arrival_date: datetime) -> list[FlightResponse]:
    formatted_date = arrival_date.strftime("%Y-%m-%d")
    # Else make request
    API_URL = f"https://api-dp-prod.dp.heathrow.com/pihub/flights/arrivals?date={formatted_date}&orderBy=localArrivalTime&excludeCodeShares=true"
    response = requests.get(API_URL, headers=headers)
    return cast(list[FlightResponse], json.loads(response.text))


def filter_non_privileged_flights(flight_infos: list) -> list:
    return [
        flight
        for flight in flight_infos
        if flight["origin_airport"] not in get_all_privileged_airports()
    ]


def calculate_hourly_congestion(
    flight_infos: list, reference_date: datetime
) -> dict[str, int]:
    histogram = {}
    for hour in range(24):
        start = reference_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=1)
        passengers = sum(
            flight["estimated_passengers"]
            for flight in flight_infos
            if start <= datetime.fromisoformat(flight["arrival_time"]) < end
        )
        histogram[start.strftime("%H:%M")] = passengers
    return histogram


def visualize_congestion(congestion: dict):
    hours = list(congestion.keys())
    counts = list(congestion.values())

    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts)
    plt.title("Hourly Congestion for Non-Privileged Flights")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Flights")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    reference_date = datetime.now() + timedelta(days=5)

    # Fetch arrivals data
    arrivals_data = get_arrivals(reference_date)
    all_flights = parse_response(arrivals_data)

    # Filter out privileged flights
    non_privileged_flights = filter_non_privileged_flights(all_flights)

    # Calculate hourly congestion
    congestion = calculate_hourly_congestion(non_privileged_flights, reference_date)

    # Create DataFrame for all flights and non-privileged flights
    df_all = pd.DataFrame(all_flights)
    df_non_privileged = pd.DataFrame(non_privileged_flights)

    print("All flights:")
    print(df_all)
    print("\nNon-privileged flights:")
    print(df_non_privileged)
    print("\nHourly congestion for non-privileged flights:")
    print(congestion)

    # Visualize the congestion
    visualize_congestion(congestion)
