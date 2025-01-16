import pandas as pd
from amadeusClient import AmadeusClient
from typing import List

FILE_NAME = "flights"

df = pd.read_csv(f"{FILE_NAME}.csv")
client = AmadeusClient()
priceByFlight: List[float] = []

def getFlighPricesBasedOn(flght: List[str]):
    print(flght)
    return {"PRICE": 1550}

for i,row in df.iterrows():
    # cuidado, nós só temos 2000 chamadas à API
    #price = client.getFlighPricesBasedOn([row["Date"], row["Origin Airport"], row["Destination Airport"]])
    priceByFlight.append(price["PRICE"])

df["Price"] = priceByFlight

df.to_csv(f"{FILE_NAME}_priced.csv")





