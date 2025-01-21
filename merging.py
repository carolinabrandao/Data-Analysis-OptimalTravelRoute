import pandas as pd

# Load the results of the greedy paths
greedy_results = pd.read_csv("greedy_path_results.csv")  # Columns: Route Number, Path, Total Distance (km), Total Price

# Load the second CSV
second_csv = pd.read_csv("routes_info_optimal.csv")  # Replace with your actual file name

# Ensure matching column names for merging
greedy_results.rename(columns={'Route Number': 'Route ID'}, inplace=True)

# Adjust Path, Distance, and Prices excluding the first city
def adjust_path_distance_price(row):
    # Split the path into cities
    cities = row['Path'].split(' -> ')
    # Exclude the first city
    adjusted_cities = cities[1:]
    # Format as a list string
    adjusted_path = str(adjusted_cities)
    # Calculate the adjusted distance and price proportionally
    if len(cities) > 1:
        ratio = len(adjusted_cities) / len(cities)
        adjusted_distance = round(row['Total Distance (km)'] * ratio, 2)
        adjusted_price = round(row['Total Price'] * ratio, 2)
    else:
        adjusted_distance = round(row['Total Distance (km)'], 2)
        adjusted_price = round(row['Total Price'], 2)
    return adjusted_path, adjusted_distance, adjusted_price

# Apply the adjustment function to greedy results
greedy_results[['Adjusted Path', 'Adjusted Distance', 'Adjusted Price']] = greedy_results.apply(
    lambda row: pd.Series(adjust_path_distance_price(row)), axis=1
)

# Merge the adjusted path, distance, and price into the second CSV
merged_df = second_csv.merge(
    greedy_results[['Route ID', 'Adjusted Path', 'Adjusted Distance', 'Adjusted Price']], 
    on='Route ID', 
    how='left'
)

# Update the columns in the second CSV
merged_df['Greedy Route'] = merged_df['Adjusted Path']
merged_df['Greedy Distance'] = merged_df['Adjusted Distance']
merged_df['Greedy Price'] = merged_df['Adjusted Price']

# Drop intermediate columns
merged_df.drop(columns=['Adjusted Path', 'Adjusted Distance', 'Adjusted Price'], inplace=True)

# Save the updated CSV
merged_df.to_csv("routes_final.csv", index=False)

# Display a preview of the updated DataFrame
print(merged_df.head())
