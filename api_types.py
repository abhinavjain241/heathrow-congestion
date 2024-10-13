from typing import Optional, TypedDict


class AirportCityLocation(TypedDict):
    name: str


class ScheduledTime(TypedDict):
    utc: str
    local: str


class AirportFacility(TypedDict):
    iataIdentifier: str
    icaoIdentifier: str
    name: str
    airportCityLocation: dict[str, str]
    terminalFacility: dict[str, str]
    standFacility: dict[str, str]


class OperatingTimes(TypedDict):
    scheduled: Optional[ScheduledTime]
    estimated: Optional[ScheduledTime]
    actual: Optional[ScheduledTime]


class PortOfCall(TypedDict):
    portOfCallType: str
    airportFacility: AirportFacility
    operatingTimes: Optional[OperatingTimes]


class Route(TypedDict):
    internationalOrDomestic: str
    portsOfCall: list[PortOfCall]


class StatusData:
    localisationKey: str
    data: str


class AircraftMovementStatus(TypedDict):
    name: str
    message: str
    statusCode: str
    statusData: list[StatusData]


class AircraftMovement(TypedDict):
    scheduledFlightDurationMinutes: int
    aircraftMovementStatus: list[AircraftMovementStatus]
    route: Route
    stops: int


class AirlineParty(TypedDict):
    iataIdentifier: str
    icaoIdentifier: str
    name: str
    tailfinImageUrl: str


class AircraftTransport(TypedDict):
    iataTypeCode: str
    icaoTypeCode: str
    description: str
    type: str
    class_: str


class FlightServiceResponse(TypedDict):
    iataFlightIdentifier: str
    icaoFlightIdentifier: str
    flightNumber: str
    suffix: str
    arrivalOrDeparture: str
    codeShareStatus: str
    aircraftMovement: AircraftMovement
    airlineParty: AirlineParty
    aircraftTransport: AircraftTransport


class FlightResponse(TypedDict):
    flightService: FlightServiceResponse
