import pandas as pd
from amadeusClient import AmadeusClient
from typing import List

FILE_NAME = "flights"

# inserting the price in the flights

df = pd.read_csv(f"{FILE_NAME}.csv")
client = AmadeusClient()
priceByFlight: List[float] = []

def getFlighPricesBasedOn(flght: List[str]):
    print(flght)
    return {"PRICE": 1550}

for i,row in df.iterrows():
    price = client.getFlighPricesBasedOn([row["Date"], row["Origin Airport"], row["Destination Airport"]])
    priceByFlight.append(price["PRICE"])

df["Price"] = priceByFlight

df.to_csv(f"{FILE_NAME}_priced.csv")





