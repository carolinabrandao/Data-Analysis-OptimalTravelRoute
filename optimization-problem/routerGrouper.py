from pandas import read_csv
from typing import Dict,List


class FlightModel:
    origin: str
    destination: str
    data: str
    price: float

    def __init__(self, data: Dict[str, str]):
        self.origin = data["Origin Airport"]
        self.destination = data["Destination Airport"]
        self.price = data["Price"]
        self.data = data["Date"]
        pass

class OptimizationProblem:
    days: List[str]
    cities: List[str]
    origin: str
    flights: List[FlightModel]

    def __init__(self, data: List[FlightModel]):
        self.days = []
        self.cities = []
        self.flights = []
        days = {}
        cities = {}

        for flight in data:
            days[flight.data] = True
            cities[flight.origin] = True
            self.flights.append(flight)
            
        self.days = days.keys()
        self.cities = cities.keys()
        self.origin = self.flights[0].origin
        pass

flights = read_csv("flights_priced.csv")

flightsByRouteId: Dict[int, List[FlightModel]] = {}

#Origin City, Origin Airport, Destination City, Destination Airport, Date, Route Number, Distance (km), Price

for index, flight in flights.iterrows():
    routeId = flight["Route Number"]
    
    if flight["Route Number"] not in flightsByRouteId:
        flightsByRouteId[routeId] = []
    
    flightsByRouteId[routeId].append(FlightModel(flight))

problems: Dict[int, List[OptimizationProblem]] = {}

for routeId in flightsByRouteId:
    problems[routeId] = OptimizationProblem(flightsByRouteId[routeId])

