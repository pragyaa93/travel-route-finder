# dataset_generator.py
"""
Generates a reproducible city list and a symmetric distance CSV file.
Run this once to create 'city_distances.csv'.
"""

import csv
import random

def get_city_list():
    return [
        # NCR & Haryana/Punjab/Rajasthan nearby
        "Delhi","Gurugram","Noida","Ghaziabad","Faridabad","Sonipat","Panipat",
        "Meerut","Rewari","Bahadurgarh","Rohtak","Bhiwadi",
        # UP
        "Agra","Mathura","Lucknow","Kanpur","Varanasi","Prayagraj","Bareilly","Moradabad",
        # Rajasthan
        "Jaipur","Alwar","Ajmer","Kota","Udaipur","Jodhpur","Bikaner",
        # Haryana/others
        "Hisar","Ambala","Karnal","Kurukshetra",
        # Punjab
        "Chandigarh","Ludhiana","Amritsar","Patiala",
        # Major metros
        "Mumbai","Pune","Ahmedabad","Surat","Vadodara","Indore","Bhopal","Nagpur",
        "Hyderabad","Visakhapatnam","Chennai","Bengaluru","Kolkata","Guwahati","Patna","Ranchi"
    ]

def approx_distance_matrix(cities, seed=42):
    random.seed(seed)
    n = len(cities)

    north_cluster = set(["Delhi","Gurugram","Noida","Ghaziabad","Faridabad","Sonipat","Panipat",
                         "Meerut","Rewari","Bahadurgarh","Rohtak","Bhiwadi","Hisar","Ambala","Karnal","Kurukshetra",
                         "Chandigarh","Ludhiana","Amritsar","Patiala"])
    up_cluster = set(["Agra","Mathura","Lucknow","Kanpur","Varanasi","Prayagraj","Bareilly","Moradabad"])
    raj_cluster = set(["Jaipur","Alwar","Ajmer","Kota","Udaipur","Jodhpur","Bikaner"])
    metros = set(["Mumbai","Pune","Ahmedabad","Surat","Vadodara","Indore","Bhopal","Nagpur",
                  "Hyderabad","Visakhapatnam","Chennai","Bengaluru","Kolkata","Guwahati","Patna","Ranchi"])

    def dist(a,b):
        if a == b: return 0
        if a in north_cluster and b in north_cluster:
            return random.randint(30,150)
        if a in up_cluster and b in up_cluster:
            return random.randint(80,300)
        if a in raj_cluster and b in raj_cluster:
            return random.randint(80,350)
        if a in metros and b in metros:
            return random.randint(500,1600)
        if (a in north_cluster and b in up_cluster) or (a in up_cluster and b in north_cluster):
            return random.randint(150,500)
        if (a in north_cluster and b in raj_cluster) or (a in raj_cluster and b in north_cluster):
            return random.randint(150,450)
        if (a in up_cluster and b in raj_cluster) or (a in raj_cluster and b in up_cluster):
            return random.randint(250,700)
        if (a in (north_cluster|up_cluster|raj_cluster) and b in metros) or (b in (north_cluster|up_cluster|raj_cluster) and a in metros):
            return random.randint(800,1700)
        return random.randint(300,1400)

    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            d = dist(cities[i], cities[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix

def write_csv(cities, matrix, filename="city_distances.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["city"] + cities
        writer.writerow(header)
        for city, row in zip(cities, matrix):
            writer.writerow([city] + row)
    print(f"Wrote {filename} with {len(cities)} cities.")

if __name__ == "__main__":
    cities = get_city_list()
    mat = approx_distance_matrix(cities, seed=42)
    write_csv(cities, mat)
