#take two columns from one csv file and merge them into another csv file

import pandas as pd
import os

# Nome dos arquivos CSV
csv_file1 = 'final.csv'
csv_file2 = 'routes_final.csv'

# Verifica se os arquivos já existem
if not os.path.exists(csv_file1):
    # Cria o arquivo inicial se não existir
    columns = [
        "Route ID", "Start City", "Start Date", "Greedy Route", "Optimal Route",
        "Greedy Price", "Optimal Price", "Season", "Target Audience", "Region", "Subregion","Month"
    ]
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file1, index=False)
    print(f"Arquivo criado: {csv_file1}")

if not os.path.exists(csv_file2):
    # Cria o arquivo inicial se não existir
    columns = [
        "Route ID", "Start City", "Start Date", "Greedy Route", "Optimal Route",
        "Greedy Price", "Optimal Price", "Season", "Target Audience", "Region", "Subregion","Month"
    ]
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file2, index=False)
    print(f"Arquivo criado: {csv_file2}")


#put columns Greedy Distance and Optimal Route Distance from csv file1 into csv file2, replacing the greedy and creating a new column for optimal
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)

df2['Greedy Distance'] = df1['Greedy Distance']
df2['Optimal Distance'] = df1['Optimal Distance']

df2.to_csv(csv_file2, index=False)
print(f"Arquivo '{csv_file2}' atualizado com sucesso!")

