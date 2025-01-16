import csv
from datetime import datetime, timedelta
from itertools import permutations
import cloudscraper
from bs4 import BeautifulSoup

def get_distance(origin, destination, distance_cache):
    # Check cache first
    pair = tuple(sorted([origin, destination]))
    if pair in distance_cache:
        return distance_cache[pair]

    # scraper to bypass cloudflare
    scraper = cloudscraper.create_scraper()

    url = f"https://www.distance.to/{origin}/{destination}"
    response = scraper.get(url)

    # process the html
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the distance element
    distance_element = soup.find("span", class_="value km")
    if distance_element:  # turn the distance into float
        distance = float(distance_element.text.replace(",", ""))
        distance_cache[pair] = distance  # Cache the result
        return distance
    else:
        distance_cache[pair] = None
        return None

def get_flight_info():
    print("Enter the origin city and its airport code:")
    origin_city = input("Origin City: ")
    origin_airport = input(f"Airport code for {origin_city}: ")

    num_destinations = int(input("\nHow many destination cities will you visit? "))

    destinations = []
    for i in range(num_destinations):
        destination_city = input(f"Destination City {i + 1}: ")
        destination_airport = input(f"Airport code for {destination_city}: ")
        destinations.append((destination_city, destination_airport))

    start_date = input("\nEnter the starting flight date (YYYY/MM/DD): ")
    route_number = input("\nEnter the route number: ")

    return origin_city, origin_airport, destinations, start_date, route_number

def generate_flight_combinations(origin, origin_code, destinations, start_date, route):
    start_date_obj = datetime.strptime(start_date, "%Y/%m/%d")
    flight_data = []
    unique_rows = set()
    distance_cache = {}

    destination_permutations = permutations(destinations)

    for perm in destination_permutations:
        current_date = start_date_obj
        trip = [(origin, origin_code)] + list(perm) + [(origin, origin_code)]
        for i in range(len(trip) - 1):
            current_city, current_code = trip[i]
            next_city, next_code = trip[i + 1]
            flight_date = current_date.strftime("%Y/%m/%d")
            distance = get_distance(current_city, next_city, distance_cache)

            row = (
                current_city, current_code, next_city, next_code, flight_date, route, distance, 0
            )

            if row not in unique_rows:
                unique_rows.add(row)
                flight_data.append({
                    "Origin City": current_city,
                    "Origin Airport": current_code,
                    "Destination City": next_city,
                    "Destination Airport": next_code,
                    "Date": flight_date,
                    "Route Number": route,
                    "Distance (km)": distance,
                    "Price": 0
                })

            current_date += timedelta(days=4)

    return flight_data

def save_to_csv(flight_data, filename="flights.csv"):
    file_exists = False
    try:
        with open(filename, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode="a" if file_exists else "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=flight_data[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(flight_data)

    print(f"\nFlight data saved to {filename}.")

def main():
    origin_city, origin_airport, destinations, start_date, route_number = get_flight_info()
    flight_data = generate_flight_combinations(origin_city, origin_airport, destinations, start_date, route_number)
    save_to_csv(flight_data)

if __name__ == "__main__":
    main()
