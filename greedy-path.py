import pandas as pd

# Load the main CSV
routes_df = pd.read_csv("flights.csv")

# Load the starting city for each route number
start_city_df = pd.read_csv("routes_info_optimal.csv") 

def find_greedy_path(df, start_city):
    # Create a copy of the DataFrame
    unvisited_cities = set(df['Destination City'].unique())
    visited_cities = [start_city]
    unvisited_cities.discard(start_city)
    total_distance = 0
    total_price = 0
    
    current_city = start_city

    while unvisited_cities:
        # Filter routes from the current city
        possible_routes = df[df['Origin City'] == current_city]
        # Find the closest unvisited city
        possible_routes = possible_routes[possible_routes['Destination City'].isin(unvisited_cities)]
        if possible_routes.empty:
            break  # No more unvisited cities reachable

        next_route = possible_routes.loc[possible_routes['Distance (km)'].idxmin()]
        next_city = next_route['Destination City']
        distance = next_route['Distance (km)']
        price = next_route['Price']
        
        # Update visited and unvisited cities
        visited_cities.append(next_city)
        unvisited_cities.discard(next_city)
        total_distance += distance
        total_price += price

        # Move to the next city
        current_city = next_city

    return visited_cities, total_distance, total_price

# Initialize results dictionary
results = []

# Group the data by route number
grouped_routes = routes_df.groupby('Route Number')

for route_number, group in grouped_routes:
    # Get the starting city for this route number
    start_city_row = start_city_df[start_city_df['Route ID'] == route_number]
    if start_city_row.empty:
        continue  # Skip if no start city is defined for this route number
    start_city = start_city_row['Start City'].iloc[0]
    
    # Apply the greedy algorithm for the current route
    path, total_distance, total_price = find_greedy_path(group, start_city)
    
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
results_df.to_csv("greedy_path_results.csv", index=False)

# Display the results
print(results_df)
