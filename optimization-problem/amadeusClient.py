import requests
import credentials
from typing import Dict, List
import json

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

    def getFlighPricesBasedOn(self, flights: List[List[str]]):
        
        token = self._authenticate()

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            'Content-Type': 'application/json',
            'X-HTTP-Method-Override': 'GET',
            'Authorization': f"{token['token_type']} {token['access_token']}"
        }

        payload = json.dumps(self._createPayloadBasedOn(flights))


        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    
    def _createPayloadBasedOn(self, flights:  List[List[str]]):
        return {
            "currencyCode": "USD",
            "originDestinations": [
                {
                "id": "1",
                "originLocationCode": "BOS",
                "destinationLocationCode": "MAD",
                "departureDateTimeRange": {
                    "date": "2025-01-01",
                    "time": "10:00:00"
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
                {
                "id": "2",
                "travelerType": "CHILD",
                "fareOptions": [
                    "STANDARD"
                ]
                }
            ],
            "sources": [
                "GDS"
            ],
            "searchCriteria": {
                "maxFlightOffers": 2,
                "flightFilters": {
                "cabinRestrictions": [
                    {
                    "cabin": "BUSINESS",
                    "coverage": "MOST_SEGMENTS",
                    "originDestinationIds": [
                        "1"
                    ]
                    }
                ],
                "carrierRestrictions": {
                    "excludedCarrierCodes": [
                    "AA",
                    "TP",
                    "AZ"
                    ]
                }
                }
            }
        }


