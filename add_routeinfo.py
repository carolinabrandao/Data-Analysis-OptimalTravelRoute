import pandas as pd
import os

csv_file = 'routes_info.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(csv_file):
    columns = [
        "Route ID", "Start City", "Start Date", "Greedy Route", "Optimal Route",
        "Greedy Price", "Optimal Price", "Season", "Target Audience", "Region", "Subregion","Month"
    ]
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)
    print(f"Arquivo criado: {csv_file}")

# Function to add a new route
def add_route():
    df = pd.read_csv(csv_file)
    
    print("Add a new route:")
    route_id = input("Route ID: ")
    start_city = input("Start City: ")
    start_date = input("Start Date (YYYY-MM-DD): ")
    season = input("Season (SUMMER/WINTER): ")
    target_audience = input("Target Audience (YOUNG/ELDER): ")
    region = input("Region (EUROPE/USA): ")
    subregion = input("Subregion (EAST/WEST): ")
    month = input("Month (JUNE/JULY): ")
    
    # Create a new route DataFrame
    new_route = pd.DataFrame([{
        "Route ID": route_id,
        "Start City": start_city,
        "Start Date": start_date,
        "Greedy Route": "",
        "Optimal Route": "",
        "Greedy Price": "",
        "Optimal Price": "", 
        "Season": season.upper(),
        "Target Audience": target_audience.upper(),
        "Region": region.upper(),
        "Subregion": subregion.upper(),
        "Month": month.upper()
    }])
    
    # Add the new route to the existing DataFrame
    df = pd.concat([df, new_route], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)
    print(f"Successfully added the route to '{csv_file}'!")

while True:
    add_route()
    cont = input("Do you want to add a new route? (Y/N): ").strip().upper()
    if cont != 'Y':
        break
