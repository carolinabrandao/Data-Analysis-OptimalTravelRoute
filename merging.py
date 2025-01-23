import pandas as pd

# Load the results of the greedy paths
greedy_results = pd.read_csv("greedy_path.csv")  # Columns: Route Number, Path, Total Distance (km), Total Price

# Load the second CSV
second_csv = pd.read_csv("routes_info_optimal.csv")  # Replace with your actual file name

# Ensure matching column names for merging
greedy_results.rename(columns={'Route Number': 'Route ID'}, inplace=True)

# Format the Greedy Route column to match Optimal Route format, excluding the first city
def format_greedy_route(route):
    # Split the route by ' -> ' and exclude the first city
    cities = route.split(' -> ')[1:]  # Exclude the first city
    return str(cities)

greedy_results['Formatted Greedy Route'] = greedy_results['Path'].apply(format_greedy_route)

# Merge the results from the greedy paths into the second CSV
merged_df = second_csv.merge(
    greedy_results[['Route ID', 'Formatted Greedy Route', 'Total Distance (km)', 'Total Price']], 
    on='Route ID', 
    how='left'
)

# Update the columns in the second CSV
merged_df['Greedy Route'] = merged_df['Formatted Greedy Route']
merged_df['Greedy Distance'] = merged_df['Total Distance (km)']
merged_df['Greedy Price'] = merged_df['Total Price'].apply(lambda x: round(x, 2))

# Drop intermediate columns, the 'ID' column, and any unnecessary ones
merged_df.drop(columns=['Formatted Greedy Route', 'Total Distance (km)', 'Total Price', 'ID'], inplace=True)

# Save the updated CSV
merged_df.to_csv("routes_final.csv", index=False)

# Display a preview of the updated DataFrame
print(merged_df.head())