import cloudscraper
from bs4 import BeautifulSoup

#function to get the distance between two cities using the distance.to website
def get_distance(origin, destination):
    
    #scraper to bypass cloudflare
    scraper = cloudscraper.create_scraper()

    url = f"https://www.distance.to/{origin}/{destination}"
    response = scraper.get(url)

    #process the html
    soup = BeautifulSoup(response.text, 'html.parser')

    #find the distance element
    distance_element = soup.find("span", class_="value km")
    if distance_element: #turn the distance into float
        return float(distance_element.text.replace(",", ""))
        #if conversion fails, return the string

    else:
        return distance_element
    
#function to simulate a greedy route that people would usually take
def greedy_route(departure_city, cities, distances):
    visited = [departure_city]  #list of visited cities, starting with only the departure city
    total_distance = 0.0  #total distance of the route
    current_city = departure_city  #current city is the departure city

    #while there are cities that haven't been visited
    while len(visited) < len(cities):
        
        #finding the nearest city
        nearest_city = None
        nearest_distance = float("inf")  

        for city in cities:
            if city not in visited: 
                combination = str([current_city, city])
                reverse_combination = str([city, current_city])

                #searches in the dic both the combination and the reverse combination
                distance = distances.get(combination) or distances.get(reverse_combination)

                if distance and distance < nearest_distance:
                    nearest_distance = distance
                    nearest_city = city

        #updates the visited list and the total distance
        if nearest_city:
            visited.append(nearest_city)
            total_distance += nearest_distance
            current_city = nearest_city  #current city is now the nearest city found
        else:
            print("Erro: Não foi possível encontrar uma cidade próxima.")
            break

    return visited, total_distance


num_cities = int(input("Enter the number of cities you want to visit: "))

departure_city = input("Enter the city you are departing from: ")

#list of cities
cities = []
cities.append(departure_city)

for i in range(num_cities):
    if i == 0:
        city = input("Enter the first city you want to visit: ") 
    elif i == 1:
        city = input("Enter the second city you want to visit: ") 
    elif i == 2:
        city = input("Enter the third city you want to visit: ") 
    else: 
        city = input(f"Enter the {i+1}th city you want to visit: ")
    
    cities.append(city)


#write on collected-data.txt the cities
with open("collected-data.txt", "a") as file:
 
    file.write("Departure city: " + departure_city + "\n")
    #write the cities in the file without the departure city
    file.write("Cities to visit: " + ", ".join(cities[1:]) + "\n")




#list of unique combinations of two cities
combinations = []
for i in range(len(cities)):
    for j in range(i+1, len(cities)):
        combination = [cities[i], cities[j]]
        combinations.append(combination)


#dic where the key is the combination and the value is the distance between the two cities in the combination
distances = {}
for combination in combinations:
    origin = combination[0]
    destination = combination[1]
    distance = get_distance(origin, destination)
    distances[str(combination)] = distance

#write on collected-data.txt the distances
with open("collected-data.txt", "a") as file:
    file.write("\nDistances:\n")
    for key, value in distances.items():
        file.write(key + " " + str(value) + "\n")



route, total_distance = greedy_route(departure_city, cities, distances)

#write on collected-data.txt the greedy route and the total distance
with open("collected-data.txt", "a") as file:
    file.write("\nGreedy route: " + " -> ".join(route) + "\n")
    file.write("Total distance: " + str(total_distance) + " km\n\n")
    file.write("------------------------------------------------------------\n")
