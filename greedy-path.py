import pandas as pd
from datetime import timedelta

routes_df = pd.read_csv("flights.csv")

routes_df['Date'] = pd.to_datetime(routes_df['Date'])

# Load the starting city and date for each route number
start_city_df = pd.read_csv("routes_info_optimal.csv")
start_city_df['Start Date'] = pd.to_datetime(start_city_df['Start Date'])

def find_greedy_path_with_distances(df, start_city, start_date):
    """
    Find the greedy path starting from a city, considering only closest distances,
    and calculate prices of the greedy route.
   
    Returns:
        tuple: (visited cities, total distance, total price)
    """
    unvisited_cities = set(df['Destination City'].unique())
    visited_cities = [start_city]
    unvisited_cities.discard(start_city)
    total_distance = 0
    total_price = 0
    current_city = start_city
    current_date = start_date

    while unvisited_cities:
        # Filter routes from the current city
        possible_routes = df[df['Origin City'] == current_city]
        # Find the closest unvisited city by distance
        possible_routes = possible_routes[possible_routes['Destination City'].isin(unvisited_cities)]
        
        if possible_routes.empty:
            break  # No more unvisited cities reachable

        # Select the route with the shortest distance
        next_route = possible_routes.loc[possible_routes['Distance (km)'].idxmin()]
        next_city = next_route['Destination City']
        distance = next_route['Distance (km)']

        # Find the price for this leg based on the travel date
        available_flights = possible_routes[possible_routes['Destination City'] == next_city]
        flight_on_date = available_flights[available_flights['Date'] == current_date]
        
        if flight_on_date.empty:
            # No flight available on the required date; stop the route
            break
        
        # Take the price of the first valid flight after the current date
        price = flight_on_date.iloc[0]['Price']

        # Update visited and unvisited cities
        visited_cities.append(next_city)
        unvisited_cities.discard(next_city)
        total_distance += distance
        total_price += price

        # Move to the next city and increment the travel date by 4 days
        current_city = next_city
        current_date += timedelta(days=4)

    # Add the price for the return leg without modifying the path
    possible_routes = df[df['Origin City'] == current_city]
    return_flights = possible_routes[possible_routes['Destination City'] == start_city]
    return_flight_on_date = return_flights[return_flights['Date'] == current_date]

    if not return_flight_on_date.empty:
        # If a return flight is available, add the price and distance back to the total
        return_flight = return_flight_on_date.iloc[0]
        return_price = return_flight['Price']
        total_price += return_price
        total_distance += return_flight['Distance (km)']

    return visited_cities, round(total_distance,2), round(total_price,2)


results = []

# Group the data by route number
grouped_routes = routes_df.groupby('Route Number')

for route_number, group in grouped_routes:
    # Get the starting city and date for this route number
    start_city_row = start_city_df[start_city_df['Route ID'] == route_number]
    if start_city_row.empty:
        continue  # Skip if no start city is defined for this route number
    start_city = start_city_row['Start City'].iloc[0]
    start_date = start_city_row['Start Date'].iloc[0]
    
    # Apply the greedy algorithm for the current route
    path, total_distance, total_price = find_greedy_path_with_distances(group, start_city, start_date)
    
    # Store the results
    results.append({
        "Route Number": route_number,
        "Path": " -> ".join(path),
        "Total Distance (km)": total_distance,
        "Total Price": total_price
    })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)

# Save the results to a CSV
results_df.to_csv("greedy_path.csv", index=False)