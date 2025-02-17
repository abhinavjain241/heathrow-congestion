from datetime import datetime, timedelta
from enum import Enum
from functools import cache
from typing import Dict, List, Tuple, cast
import requests
import json

from api_types import AirportFacility, FlightResponse, FlightServiceResponse, PortOfCall
from data import get_all_privileged_airports, plane_types


class PortOfCallType(Enum):
    ORIGIN = "ORIGIN"
    DESTINATION = "DESTINATION"


class FlightDataFetcher:
    def __init__(self):
        self.headers = {
            "authority": "api-dp-prod.dp.heathrow.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "origin": "https://www.heathrow.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }

    @staticmethod
    def get_port_of_call(portsOfCall: list, type: PortOfCallType) -> PortOfCall:
        return next(
            (
                portOfCall
                for portOfCall in portsOfCall
                if portOfCall["portOfCallType"] == type.value
            ),
            None,
        )

    @staticmethod
    def get_airport(portOfCall: PortOfCall) -> Tuple[str, str]:
        airportFacility: AirportFacility = portOfCall["airportFacility"]
        airport_id = airportFacility.get("iataIdentifier", "")
        airport_city = airportFacility["airportCityLocation"].get("name", "")
        return airport_id, airport_city

    @staticmethod
    def get_scheduled_time(portOfCall: PortOfCall) -> str:
        if (
            "operatingTimes" in portOfCall
            and "scheduled" in portOfCall["operatingTimes"]
        ):
            return portOfCall["operatingTimes"]["scheduled"]["local"]
        return None

    @staticmethod
    def get_plane_type(flight_service: FlightServiceResponse) -> str:
        if (
            "aircraftTransport" not in flight_service
            or "description" not in flight_service["aircraftTransport"]
        ):
            return ""
        return flight_service["aircraftTransport"]["description"]

    @staticmethod
    def get_flight_carrier(flight_service: FlightServiceResponse) -> str:
        if (
            "airlineParty" not in flight_service
            or "name" not in flight_service["airlineParty"]
        ):
            return ""
        return flight_service["airlineParty"]["name"]

    @staticmethod
    def estimate_passengers(plane_type: str) -> int:
        if plane_type in plane_types:
            min_capacity, max_capacity = plane_types[plane_type]
            return (min_capacity + max_capacity) // 2  # Use average capacity
        return 200  # Default estimate if plane type is unknown

    def parse_response(self, response: List[FlightResponse]) -> List[Dict]:
        flight_infos = []
        for flight in response:
            flight_service: FlightServiceResponse = flight["flightService"]
            aircraftMovement = flight_service["aircraftMovement"]
            if aircraftMovement is not None and "route" in aircraftMovement:
                route = aircraftMovement["route"]
                if route is not None and "portsOfCall" in route:
                    portsOfCall = route["portsOfCall"]
                    origin = self.get_port_of_call(portsOfCall, PortOfCallType.ORIGIN)
                    destination = self.get_port_of_call(
                        portsOfCall, PortOfCallType.DESTINATION
                    )
                    origin_airport, origin_city = self.get_airport(origin)
                    arrival_time = self.get_scheduled_time(
                        destination
                    )  # Arrival in LHR
                    plane_type = self.get_plane_type(flight_service)
                    estimated_passengers = self.estimate_passengers(plane_type)
                    flight_infos.append(
                        {
                            "flightNumber": flight_service["iataFlightIdentifier"],
                            "flightCarrier": self.get_flight_carrier(flight_service),
                            "planeType": plane_type,
                            "origin_airport": origin_airport,
                            "origin_city": origin_city,
                            "arrival_time": arrival_time,
                            "estimated_passengers": estimated_passengers,
                        }
                    )
        return flight_infos

    @cache
    def get_arrivals(self, arrival_date: datetime) -> List[FlightResponse]:
        formatted_date = arrival_date.strftime("%Y-%m-%d")
        API_URL = f"https://api-dp-prod.dp.heathrow.com/pihub/flights/arrivals?date={formatted_date}&orderBy=localArrivalTime&excludeCodeShares=true"
        response = requests.get(API_URL, headers=self.headers)
        return cast(List[FlightResponse], json.loads(response.text))

    @staticmethod
    def filter_non_privileged_flights(flight_infos: List[Dict]) -> List[Dict]:
        return [
            flight
            for flight in flight_infos
            if flight["origin_airport"] not in get_all_privileged_airports()
        ]
