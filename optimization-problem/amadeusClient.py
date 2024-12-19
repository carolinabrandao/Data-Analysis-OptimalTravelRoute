import requests
import credentials
from typing import Dict, List
import json
from math import pow

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

class AmadeusClient:
    def _authenticate(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": credentials.KEY,
            "client_secret": credentials.SECRET
        }

        response_token = requests.post(TOKEN_URL, headers=headers, data=data)

        #'token_type': 'Bearer', 'access_token': 'v2b8gQUG5UrrDsIA5G1zKVlDVQm4'
        token: Dict[str, str] = response_token.json()

        return token

    def getFlighPricesBasedOn(self, flights: List[str]):
        
        token = self._authenticate()

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            'Content-Type': 'application/json',
            'X-HTTP-Method-Override': 'GET',
            'Authorization': f"{token['token_type']} {token['access_token']}"
        }

        payload = json.dumps(self._createPayloadBasedOn(flights))

        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
            return { "VALID": True, "PRICE": response["data"][0]["price"]["total"]}
        except:
            return { "VALID": False, "PRICE": pow(10,10)}
    
    def _createPayloadBasedOn(self, flight: List[str]):
        return {
            "currencyCode": "EUR",
            "originDestinations": [
                {
                "id": "1",
                "originLocationCode": flight[1],
                "destinationLocationCode": flight[2],
                "oneWay": True,
                "departureDateTimeRange": {
                    "date": flight[0]
                }
                }
            ],
            "travelers": [
                {
                "id": "1",
                "travelerType": "ADULT",
                "fareOptions": [
                    "STANDARD"
                ]
                },
            ],
            "sources": [
                "GDS"
            ],
            "searchCriteria": {
                "maxFlightOffers": 1
            }
        }