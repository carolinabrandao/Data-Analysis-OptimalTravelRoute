from numpy import random
from gurobipy import Model, GRB, quicksum
from plot import plot_route_with_labels

numero_de_cidades = 10
cities = [c for c in range(0,numero_de_cidades)]
days = [d for d in range(1, numero_de_cidades + 2)]


last_day = days[len(days) - 1]

cities_in_time = [(c,d) for c in cities for d in days]

edges = [((c0,t0),(c1,t1)) for (c0,t0) in cities_in_time for (c1,t1) in cities_in_time if c0 != c1 and t1 > t0]

costs = { e : random.randint(2,5) for e in edges }

for e in edges:
    if e[0][0] == 0 and e[0][1] == 1:
        costs[e] = 100
    else:
        costs[e] = random.randint(2,5)

model = Model("Problema de Otimização com Tempo")

x = model.addVars(edges, vtype=GRB.BINARY, name="x")
u = model.addVars(cities_in_time, vtype=GRB.CONTINUOUS)

model.setObjective(quicksum(costs[e] * x[e] for e in edges), GRB.MINIMIZE)

# uma cidade só deve ser visitada uma vez
for c in cities:
    model.addConstr(quicksum(x[e] for e in edges if e[1][0] == c) == 1, f"visiting_{c}")
    model.addConstr(quicksum(x[e] for e in edges if e[0][0] == c) == 1, f"departing_from_{c}")

# garantindo que eu saia da cidade 0 no primeiro dia e chegue na cidade zero no último dia
model.addConstr(quicksum(x[e] for e in edges if e[0][0] == 0 and e[0][1] == days[0]) == 1, f"departing_base_{0}")
model.addConstr(quicksum(x[e] for e in edges if e[1][0] == 0 and e[1][1] == last_day) == 1, f"visiting_base_{0}")

# garantir que eu esteja em somente uma cidade por vez
for d in days:
    ""
    # ninguém chega do primeiro dia
    if d > 1:
        model.addConstr(quicksum(x[e] for e in edges if e[1][1] == d) == 1, f"visiting_day_{d}")
    # ninguém viaja no último dia
    if d < last_day:
        model.addConstr(quicksum(x[e] for e in edges if e[0][1] == d) == 1, f"departing_day_{d}")

# garantindo que toda cidade acessada em um dado dia será também o ponto de partida de uma viagem nesse mesmo dia
model.addConstrs(
    (quicksum(x[(c0,cx)] for cx in cities_in_time if c0[0] != cx[0] and c0[1] < cx[1]) -
    quicksum(x[(cy,c0)] for cy in cities_in_time if c0[0] != cy[0] and c0[1] > cy[1])) == 0
    for c0 in cities_in_time if c0[0] != 0)

# sub tour restriction
model.addConstrs( (x[(c0,c1)] == 1) >> (u[c0] + 1 == u[c1]) for (c0,c1) in edges if c0[0]!= 0 and c1[0]!= 0 )

model.Params.LogToConsole = 1
model.optimize()


if model.status == GRB.OPTIMAL:
    solution = [(e[0][0], e[1][0]) for e in edges if x[e].x > 0.5]
    labels = { e[0][0] : f"travel {e}" for e in edges if x[e].x > 0.5 }
    plot_route_with_labels(solution, start_node=0, end_node=0, node_labels=labels)
    print([e for e in edges if x[e].x > 0.5])

if model.status == GRB.INFEASIBLE:
    model.computeIIS()
    model.write("infeasibility.ilp")
