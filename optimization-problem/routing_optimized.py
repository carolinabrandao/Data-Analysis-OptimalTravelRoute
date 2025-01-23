from numpy import random
from gurobipy import Model, GRB, quicksum
from plot import plot_route_with_labels
from models import OptimizationProblem, FlightModel
from typing import List

def solve(problem: OptimizationProblem) -> List[FlightModel]:
    cities_ = list(problem.cities)
    days_ = list(problem.days)
    i = 1

    day_to_index = {}
    for d in days_:
        day_to_index[d] = i
        i += 1

    i = 0
    city_to_index = { }
    for c in cities_:
        city_to_index[c] = i
        i += 1

    costs_indexed = {}
    for flight in problem.flights:
        costs_indexed[((city_to_index[flight.origin], day_to_index[flight.data]), (city_to_index[flight.destination], day_to_index[flight.data] + 1))] = flight.price

    numero_de_cidades = len(problem.cities)
    cities = [c for c in range(0,numero_de_cidades)]
    days = [d for d in range(1, numero_de_cidades + 2)]

    last_day = days[len(days) - 1]

    cities_in_time = [(c,d) for c in cities for d in days]
    edges = [((c0,t0),(c1,t1)) for (c0,t0) in cities_in_time for (c1,t1) in cities_in_time if c0 != 0 and c1 != 0 and c0 != c1 and t1 == (t0 + 1)]

    for c in cities:
        if c > 0:
            edges.append(((0, days[0]), (c, days[1])))
            edges.append(((c, last_day - 1), (0, last_day)))

    costs = {  }
    t = 0
    i = 0
    for e in edges:
        if e in costs_indexed:
            costs[e] = costs_indexed[e]
            t += 1 
        else:
            costs[e] = 10000
            i += 1

    if True:
        model = Model("Problema de Otimização com Tempo")

        x = model.addVars(edges, vtype=GRB.BINARY, name="x")

        model.setObjective(quicksum(costs[e] * x[e] for e in edges), GRB.MINIMIZE)

        # one city should be visited just one time
        for c in cities:
            model.addConstr(quicksum(x[e] for e in edges if e[0][0] == c) == 1, f"departing_from_{c}")
            model.addConstr(quicksum(x[e] for e in edges if e[1][0] == c) == 1, f"visiting_{c}")

        # A person should be in just one city per day
        for d in days:
            ""
            # no travels happens on the first day
            if d > 1:
                model.addConstr(quicksum(x[e] for e in edges if e[1][1] == d) == 1, f"visiting_day_{d}")
            # no travels happens on the last day
            if d < last_day:
                model.addConstr(quicksum(x[e] for e in edges if e[0][1] == d) == 1, f"departing_day_{d}")

        # ensuring that every destination is also an origin of another travel in the same day
        # also this ensure that every route created in a correct time order, considering that the date only has as initial travels 
        # (0,0) to (c, 1) -> being c any city 
        model.addConstrs(
            (quicksum(x[(c0,cx)] for cx in cities_in_time if (cx[0] != 0 or cx[1] == last_day) and c0[0] != cx[0] and (c0[1] + 1) == cx[1]) -
            quicksum(x[(cy,c0)] for cy in cities_in_time if (cy[0] != 0 or cy[1] == 1) and c0[0] != cy[0] and c0[1] == (cy[1] + 1) )) == 0
            for c0 in cities_in_time if c0[0] != 0)

        model.Params.LogToConsole = 0
        model.Params.TimeLimit = 180
        model.optimize()

        if model.status == GRB.OPTIMAL:
            return [ FlightModel({ 
                "Origin Airport" :cities_[e[0][0]], 
                "Destination Airport" : cities_[e[1][0]],
                "Date": days_[e[0][1] - 1],
                "Price": costs[e]
                }) for e in edges if x[e].x > 0.5]

        if model.status == GRB.INFEASIBLE:
            model.computeIIS()
            model.write("infeasibility.ilp")
        
        return list()
    
    pass
