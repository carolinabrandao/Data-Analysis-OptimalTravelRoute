import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper
import time

# Function to get the distance between two cities using the distance.to website
def get_distance(origin, destination):
    scraper = cloudscraper.create_scraper()
    url = f"https://www.distance.to/{origin}/{destination}"
    try:
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        distance_element = soup.find("span", class_="value km")
        if distance_element:
            try:
                return float(distance_element.text.replace(",", ""))
            except ValueError:
                return None
    except Exception as e:
        print(f"Error fetching distance from {origin} to {destination}: {e}")
        return None
    return None

file_path = 'routes_final.csv'
df = pd.read_csv(file_path)

# Calculate the optimal route distance including the return trip
def calculate_optimal_distance_with_return(row):
    cities = [row['Start City']] + eval(row['Optimal Route'])
    total_distance = 0
    for i in range(len(cities) - 1):
        distance = get_distance(cities[i], cities[i+1])
        if distance:
            total_distance += distance
        # Add a delay between requests to avoid being blocked
        time.sleep(1)
    # Add the return trip distance (last city back to start city)
    return_trip_distance = get_distance(cities[-1], row['Start City'])
    if return_trip_distance:
        total_distance += return_trip_distance
    return round(total_distance, 2)

# Add the optimal distance with return column
df['Optimal Distance with Return'] = df.apply(calculate_optimal_distance_with_return, axis=1)

# Save the updated dataframe to a new CSV
output_path = 'optimal_path_distances.csv'
df.to_csv(output_path, index=False)
