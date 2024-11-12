import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.cm as cm

# Définir la capacité maximale de chaque camion
MAX_CAPACITY_PER_TRUCK = 50  # Capacité maximale en volume

# Génération des données de villes avec volume pour chaque colis
def generate_cities(num_cities, max_volume):
    cities = []
    for _ in range(num_cities):
        x, y = np.random.uniform(0, 100, 2)  # Position de la ville
        volume = np.random.uniform(1, max_volume)  # Volume du colis
        cities.append((x, y, volume))
    return cities

# Calculer la distance entre deux villes
def distance(city1, city2):
    return np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# Parcours d'un seul camion à travers toutes les villes, retour au dépôt
def single_truck_path(cities):
    depot = cities[0]
    path = [depot] + cities[1:] + [depot]  # On passe par toutes les villes puis on retourne au dépôt
    return path

# Construire un chemin tout en respectant la capacité du camion
def assign_cities_to_trucks(cities, max_capacity):
    trucks_paths = []
    current_truck_path = []
    remaining_capacity = max_capacity

    depot = cities[0]  # L'entrepôt, premier élément de la liste

    for city in cities[1:]:
        if remaining_capacity - city[2] >= 0:  # Si la ville peut être ajoutée sans dépasser la capacité
            current_truck_path.append(city)
            remaining_capacity -= city[2]
            if remaining_capacity == 0:  # Le camion retourne au dépôt
                trucks_paths.append([depot] + current_truck_path + [depot])
                current_truck_path = []
                remaining_capacity = max_capacity
        else:
            trucks_paths.append([depot] + current_truck_path + [depot])
            current_truck_path = [city]
            remaining_capacity = max_capacity - city[2]

    if current_truck_path:  # Ajouter le dernier camion s'il reste des villes non livrées
        trucks_paths.append([depot] + current_truck_path + [depot])

    return trucks_paths

# Calcul du chemin total pour un camion
def total_distance(path):
    return sum(distance(path[i], path[i + 1]) for i in range(len(path) - 1))

# Fonction pour afficher le parcours d'un seul camion
def plot_total_path(cities):
    # Calcul du parcours complet pour un seul camion
    total_path = single_truck_path(cities)
    x_total, y_total = zip(*[(city[0], city[1]) for city in total_path])

    # Créer un graphique distinct pour le parcours total (en plein écran)
    plt.figure(figsize=(15, 12))
    plt.plot(x_total, y_total, marker='o', color='black', linestyle='-', label='Parcours total (un camion)', linewidth=2)
    plt.scatter([cities[0][0]], [cities[0][1]], color="black", s=100, label="Dépôt")  # Marquer le dépôt

    # Ajuster les limites pour afficher toutes les villes
    all_x = [city[0] for city in cities]
    all_y = [city[1] for city in cities]
    plt.xlim(min(all_x) - 5, max(all_x) + 5)
    plt.ylim(min(all_y) - 5, max(all_y) + 5)

    plt.title("Parcours total")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()

# Fonction pour afficher les parcours des camions
def plot_combined_paths(cities, trucks_paths):
    # Créer un graphique distinct pour les parcours des camions (en plein écran)
    plt.figure(figsize=(15, 12))

    # Tracer les parcours des différents camions
    colors = cm.get_cmap("tab20", len(trucks_paths))  # Palette de couleurs pour chaque camion
    line_styles = ['-', '--', '-.', ':']  # Styles de lignes différents pour chaque camion
    depot = cities[0]  # Dépôt

    for truck_id, path in enumerate(trucks_paths):
        color = colors(truck_id)
        style = line_styles[truck_id % len(line_styles)]
        x, y = zip(*[(city[0], city[1]) for city in path])

        plt.plot(x, y, marker='o', color=color, linestyle=style, label=f'Camion {truck_id + 1}')

    plt.scatter([depot[0]], [depot[1]], color="black", s=100, label="Dépôt")  # Marquer le dépôt

    # Ajuster les limites pour afficher toutes les villes
    all_x = [city[0] for city in cities]
    all_y = [city[1] for city in cities]
    plt.xlim(min(all_x) - 5, max(all_x) + 5)
    plt.ylim(min(all_y) - 5, max(all_y) + 5)

    plt.title("Parcours des camions")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()

# Fonction principale pour tester avec un seul camion et calculer le temps d'exécution
def test_solution(sizes, max_volume=10, max_capacity=MAX_CAPACITY_PER_TRUCK):
    results = []
    for size in sizes:
        cities = generate_cities(size, max_volume)
        start_time = time.time()

        # Attribution des villes aux camions selon la capacité
        trucks_paths = assign_cities_to_trucks(cities, max_capacity)

        # Calcul du parcours total
        total_path = single_truck_path(cities)

        # Calcul de la distance totale pour tous les camions
        total_distance_value = sum(total_distance(path) for path in trucks_paths)
        end_time = time.time()

        # Enregistrer les résultats
        results.append({
            "num_cities": size,
            "total_distance": total_distance_value,
            "execution_time": end_time - start_time
        })

        # Afficher le parcours total et les parcours des camions
        print(f"\nRésultats pour {size} villes :")
        print(f"Distance totale : {total_distance_value:.2f}")
        print(f"Temps d'exécution : {end_time - start_time:.2f} secondes")

        # Affichage des graphiques
        plot_total_path(cities)  # Afficher le parcours total
        plot_combined_paths(cities, trucks_paths)  # Afficher les parcours par camions

    return results

# Exécuter le test avec différentes tailles de villes
sizes = [10, 50, 100, 300, 1000]
results = test_solution(sizes)

# Afficher les résultats finaux
for result in results:
    print(f"\nNombre de villes : {result['num_cities']}")
    print(f"Distance totale : {result['total_distance']:.2f}")
    print(f"Temps d'exécution : {result['execution_time']:.2f} secondes")
