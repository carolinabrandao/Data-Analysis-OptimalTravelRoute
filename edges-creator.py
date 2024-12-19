from typing import List

def _createPossiblesDestinations(cities: List[str], origin: str, step: int = 0) -> List[str]:
    destinations = []

    for city in cities:
        destinations.append([step, origin, city])
        _cities = _removeCityFromCities(city, cities)
        destinations.extend(_createPossiblesDestinations(_cities, city, step + 1))
    
    return destinations

def _removeCityFromCities(cityToExclude: str, allCities: List[str]) -> List[str]:
    cities = []
    for city in allCities:
        if city != cityToExclude:
            cities.append(city)
    
    return cities

def createEdges(cities: List[str], origin: str) -> List[str]:
    """
    :param cities: destinations
    :param origin: origin city
    @returns: The unique edges generates by the possibles paths routes from origin to cities

    @Example
        destinations: List[str] = ["Amsterdam", "Rome", "Brussels"]
        origin: str = "Paris"
        createEdges(destinations, origin)
    """
    edges = _createPossiblesDestinations(cities, origin)
    
    for city in cities:
        edges.append([len(cities), city, origin])
    
    return edges