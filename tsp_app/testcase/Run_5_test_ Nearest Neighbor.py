import random
import math
import time

# Thuật toán TSP Nearest Neighbor (heuristic)
def tsp_nearest_neighbor(dist):
    n = len(dist)
    visited = [False] * n
    path = [0]
    visited[0] = True
    total_cost = 0

    for _ in range(n - 1):
        last = path[-1]
        next_city = None
        min_dist = float('inf')
        for city in range(n):
            if not visited[city] and dist[last][city] < min_dist:
                min_dist = dist[last][city]
                next_city = city
        path.append(next_city)
        visited[next_city] = True
        total_cost += min_dist

    # Quay lại thành phố ban đầu
    total_cost += dist[path[-1]][0]
    path.append(0)
    return total_cost, path

# Sinh tọa độ ngẫu nhiên cho các thành phố
def generate_cities(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

# Tính ma trận khoảng cách giữa các thành phố
def compute_distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.hypot(cities[i][0] - cities[j][0], cities[i][1] - cities[j][1])
    return dist

# Hàm test thuật toán Nearest Neighbor
def run_nearest_neighbor_test(n=20):
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)

    for i in range(5):  # Lặp lại 5 lần để kiểm thử
        print("-" * 50)
        print(f"Test #{i + 1}")
        start = time.time()
        cost, path = tsp_nearest_neighbor(dist)
        end = time.time()

        print(f"Time taken: {end - start:.2f} seconds")
        print(f"Chi phí: {cost:.2f}")
        print(f"Đường đi: {path}")

if __name__ == "__main__":
    run_nearest_neighbor_test(n=20)
