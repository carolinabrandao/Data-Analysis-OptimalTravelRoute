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
        # u = model.addVars(cities, vtype=GRB.CONTINUOUS)

        model.setObjective(quicksum(costs[e] * x[e] for e in edges), GRB.MINIMIZE)

        # uma cidade só deve ser visitada uma vez (em qualquer dia)
        for c in cities:
            model.addConstr(quicksum(x[e] for e in edges if e[0][0] == c) == 1, f"departing_from_{c}")
            model.addConstr(quicksum(x[e] for e in edges if e[1][0] == c) == 1, f"visiting_{c}")

        # garantindo que eu saia da cidade 0 no primeiro dia e chegue na cidade zero no último dia
        # isso passa a ser garantido pela maneira com que os dados são montados para o problema mas de qualquer forma é uma restrição importante deve estar no problema
        # assim como a restrição de subtour
        # model.addConstr(quicksum(x[e] for e in edges if e[0][0] == 0 and e[0][1] == days[0]) == 1, f"departing_base_{0}")
        # model.addConstr(quicksum(x[e] for e in edges if e[1][0] == 0 and e[1][1] == last_day) == 1, f"visiting_base_{0}")

        # garantir que eu esteja em somente uma cidade por vez
        for d in days:
            ""
            # ninguém chega do primeiro dia, ou seja, não há nenhuma viagem do tipo i,0 para j,1
            if d > 1:
                model.addConstr(quicksum(x[e] for e in edges if e[1][1] == d) == 1, f"visiting_day_{d}")
            # ninguém viaja no último dia, ou seja, não há nenhuma viagem do tipo i,d para j,d+1. d+1 não existe no nosso problema
            if d < last_day:
                model.addConstr(quicksum(x[e] for e in edges if e[0][1] == d) == 1, f"departing_day_{d}")

        # garantindo que toda cidade acessada em um dado dia será também o ponto de partida de uma viagem nesse mesmo dia
        # isso garante que o problema seja cronologicamente correto, já que sempre vamos de 0,1 para algum lugar i,1
        # dessa forma, iremos de i,1 para j,2 e assim por diante até k, d-1, para 0,d
        # além disso, subtours não podem ser formados já que toda rota começará em 0 e terminará em zero pela proposição anterior
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
