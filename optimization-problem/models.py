from typing import List, Dict

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

    def __repr__(self):
        return f"[{self.origin}, {self.destination}, {self.data}, {self.price}]"

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
    
