from pandas import read_csv
from typing import Dict,List
from routing_optimized import solve
from models import FlightModel, OptimizationProblem

flights = read_csv("flights_priced.csv")

flightsByRouteId: Dict[int, List[FlightModel]] = {}
cityByAirport: Dict[str, str] = {}

#Origin City, Origin Airport, Destination City, Destination Airport, Date, Route Number, Distance (km), Price

for index, flight in flights.iterrows():
    routeId = flight["Route Number"]
    
    if flight["Route Number"] not in flightsByRouteId:
        flightsByRouteId[routeId] = []
    
    flightsByRouteId[routeId].append(FlightModel(flight))
    cityByAirport[flight["Origin Airport"]] = flight["Origin City"]

optimalsPrice = []
paths = []

for routeId in flightsByRouteId:
    print(f"flights {len(flightsByRouteId[routeId])} from route {routeId}")
    problem = OptimizationProblem(flightsByRouteId[routeId])
    solution = solve(problem)
    optimalsPrice.append(round(sum(flight.price for flight in solution), 2))
    paths.append([cityByAirport[flight.origin] for flight in solution if flight.origin != problem.origin])


routes_df = read_csv("routes_info.csv")

routes_df["Optimal Price"] = optimalsPrice
routes_df["Optimal Route"] = paths

routes_df.to_csv("routes_info_optimal.csv")