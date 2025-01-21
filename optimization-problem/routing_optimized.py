from numpy import random
from gurobipy import Model, GRB, quicksum
from plot import plot_route_with_labels

# ["2025-01-01", "GRU", "MUC", {"VALID": true, "PRICE": "657.75"}]

costs_ = [["2025-01-01", "GRU", "MUC", {"VALID": True, "PRICE": "0"}], 
          ["2025-01-02", "MUC", "ORY", {"VALID": True, "PRICE": "0"}], 
          ["2025-01-03", "ORY", "IST", {"VALID": True, "PRICE": "10"}], 
          ["2025-01-02", "MUC", "IST", {"VALID": True, "PRICE": "72.61"}], 
          ["2025-01-03", "IST", "ORY", {"VALID": True, "PRICE": "143.27"}], 

          ["2025-01-01", "GRU", "ORY", {"VALID": True, "PRICE": "657.75"}], 
          ["2025-01-02", "ORY", "MUC", {"VALID": True, "PRICE": "120.21"}], 
          ["2025-01-03", "MUC", "IST", {"VALID": True, "PRICE": "72.61"}], 
          ["2025-01-02", "ORY", "IST", {"VALID": True, "PRICE": "138.04"}], 
          ["2025-01-03", "IST", "MUC", {"VALID": True, "PRICE": "75.12"}], 
          ["2025-01-01", "GRU", "IST", {"VALID": True, "PRICE": "787.39"}], 
          ["2025-01-02", "IST", "MUC", {"VALID": True, "PRICE": "75.12"}], 
          ["2025-01-03", "MUC", "ORY", {"VALID": True, "PRICE": "167.46"}], 
          ["2025-01-02", "IST", "ORY", {"VALID": True, "PRICE": "143.27"}], 
          ["2025-01-03", "ORY", "MUC", {"VALID": True, "PRICE": "120.21"}], 
          ["2025-01-03", "MUC", "GRU", {"VALID": True, "PRICE": "591.23"}], 

          ["2025-01-03", "ORY", "GRU", {"VALID": True, "PRICE": "521.60"}],
           
          ["2025-01-03", "IST", "GRU", {"VALID": True, "PRICE": "487.81"}]]
departing_from = "GRU"
cities_ = ["GRU", "ORY", "MUC", "IST"]
days_ = ["2025-01-01", "2025-01-02", "2025-01-03"]
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
for c in costs_:
    if city_to_index[c[2]] != 0:
        costs_indexed[((city_to_index[c[1]], day_to_index[c[0]]), (city_to_index[c[2]], day_to_index[c[0]] + 1))] = c[3]["PRICE"]
    else:
        costs_indexed[((city_to_index[c[1]], day_to_index[c[0]] + 1), (city_to_index[c[2]], day_to_index[c[0]] + 2))] = c[3]["PRICE"]

print(costs_indexed)
numero_de_cidades = 4
cities = [c for c in range(0,numero_de_cidades)]
days = [d for d in range(1, numero_de_cidades + 2)]
random.seed(42)

last_day = days[len(days) - 1]

cities_in_time = [(c,d) for c in cities for d in days]
edges = [((c0,t0),(c1,t1)) for (c0,t0) in cities_in_time for (c1,t1) in cities_in_time if c0 != 0 and c1 != 0 and c0 != c1 and t1 == (t0 + 1)]

for c in cities:
    if c > 0:
        edges.append(((0, days[0]), (c, days[1])))
        edges.append(((c, last_day - 1), (0, last_day)))

costs = {  }

for e in edges:
    if e in costs_indexed:
        costs[e] = costs_indexed[e]
    else:
        costs[e] = 100000

print(costs)
if True:
    model = Model("Problema de Otimização com Tempo")

    x = model.addVars(edges, vtype=GRB.BINARY, name="x")
    u = model.addVars(cities, vtype=GRB.CONTINUOUS)

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

    model.Params.LogToConsole = 1
    model.Params.TimeLimit = 180
    model.optimize()


    if model.status == GRB.OPTIMAL:
        solution = [(e[0][0], e[1][0]) for e in edges if x[e].x > 0.5]
        print([e[0][1] for e in edges])
        labels = { e[0][0] : f"travel {cities_[e[0][0]]} -> {cities_[e[1][0]]} at {e[0][1]}" for e in edges if x[e].x > 0.5 }
        plot_route_with_labels(solution, start_node=0, end_node=0, node_labels=labels)
        print([e for e in edges if x[e].x > 0.5])

    if model.status == GRB.INFEASIBLE:
        model.computeIIS()
        model.write("infeasibility.ilp")
