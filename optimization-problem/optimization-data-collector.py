from edgesCreator import createEdges
from amadeusClient import AmadeusClient
from time import sleep
import json

amadeusClient = AmadeusClient()
edges = createEdges(["MUC", "BRU", "MAD"], "ORY", ["2025-01-01", "2025-01-02", "2025-01-03"])

for edge in edges:
    price = amadeusClient.getFlighPricesBasedOn(edge)
    edge.extend([price])
    print(edge)
    sleep(1)

with open("flights.json", "w") as file:
    json.dump(edges, file)