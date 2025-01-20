import pandas as pd
import os

# Nome do arquivo CSV
csv_file = 'routes_info.csv'

# Verifica se o arquivo já existe
if not os.path.exists(csv_file):
    # Cria o arquivo inicial se não existir
    columns = [
        "Route ID", "Start City", "Start Date", "Greedy Route", "Optimal Route",
        "Greedy Price", "Optimal Price", "Season", "Target Audience", "Region", "Subregion","Month"
    ]
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)
    print(f"Arquivo criado: {csv_file}")

# Função para adicionar uma nova rota com campos iniciais vazios
def add_route():
    # Carrega o arquivo existente
    df = pd.read_csv(csv_file)
    
    # Solicita os dados ao usuário
    print("Adicionar uma nova rota:")
    route_id = input("Route ID: ")
    start_city = input("Start City: ")
    start_date = input("Start Date (YYYY-MM-DD): ")
    season = input("Season (SUMMER/WINTER): ")
    target_audience = input("Target Audience (YOUNG/ELDER): ")
    region = input("Region (EUROPE/USA): ")
    subregion = input("Subregion (EAST/WEST): ")
    month = input("Month (JUNE/JULY): ")
    
    # Cria um dicionário com os dados da nova rota
    new_route = pd.DataFrame([{
        "Route ID": route_id,
        "Start City": start_city,
        "Start Date": start_date,
        "Greedy Route": "",  # Campo vazio
        "Optimal Route": "",  # Campo vazio
        "Greedy Price": "",  # Campo vazio
        "Optimal Price": "",  # Campo vazio
        "Season": season.upper(),
        "Target Audience": target_audience.upper(),
        "Region": region.upper(),
        "Subregion": subregion.upper(),
        "Month": month.upper()
    }])
    
    # Concatena a nova rota ao DataFrame existente
    df = pd.concat([df, new_route], ignore_index=True)
    
    # Salva no CSV
    df.to_csv(csv_file, index=False)
    print(f"Rota adicionada com sucesso ao arquivo '{csv_file}'!")

# Loop para adicionar várias rotas
while True:
    add_route()
    cont = input("Deseja adicionar outra rota? (S/N): ").strip().upper()
    if cont != 'S':
        print("Encerrando o programa.")
        break
