from edgesCreator import createEdges
from amadeusClient import AmadeusClient
from time import sleep
import json

# São Paulo (GRU), Paris (ORY), Lisboa, Munich (MUC), Istambul (IST)
# Rio de Janeiro (GIG), Cancun (CUN), New York (NYC), San Francisco (SFO), Las Vegas (LAS)
# São Paulo (GRU), London (YXU), New York (NYC), Boston (BOS)
# Paris (ORY), Minich (MUC), Lisboa (LIS), Madrid (MAD)
# São Paulo (GRU), Santiago (SCU), Buenos Aires (BAI), Medelin (MDE), Assunção (ASU)

# Paris (ORY), singapore (SIN), Seoul (ICN), Tokyo (NRT)

routes = [
    [["MUC", "ORY", "IST"], "GRU", ["2025-01-01", "2025-01-02", "2025-01-03"], "flighs1.json"],
    [["CUN", "NYC", "SFO", "LAS"], "GIG", ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"], "flighs2.json"],
    [["YXU", "NYC", "BOS"], "GRU", ["2025-01-01", "2025-01-02", "2025-01-03"], "flighs3.json"],
    [["MUC", "LIS", "MAD"], "ORY", ["2025-01-01", "2025-01-02", "2025-01-03"], "flighs4.json"],
    [["SCU", "BAI", "MDE", "ASU"], "GRU", ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"], "flighs5.json"],
    [["SIN", "ICN", "NRT"], "ORY", ["2025-01-01", "2025-01-02", "2025-01-03"], "flighs6.json"],
]

for route in routes:
    amadeusClient = AmadeusClient()
    edges = createEdges(route[0], route[1], route[2])

    for edge in edges:
        price = amadeusClient.getFlighPricesBasedOn(edge)
        edge.extend([price])
        print(edge)
        sleep(1)

    with open(route[3], "w") as file:
        json.dump(edges, file)