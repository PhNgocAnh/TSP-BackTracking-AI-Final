import random
import math
import time

# Tạo tọa độ ngẫu nhiên cho các thành phố
def generate_cities(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

# Tính khoảng cách Euclidean giữa các thành phố
def compute_distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.hypot(cities[i][0] - cities[j][0], cities[i][1] - cities[j][1])
    return dist

# Thuật toán Backtracking
def tsp_backtracking(dist, time_limit=5):
    n = len(dist)
    best_cost = float('inf')
    best_path = None
    visited = [False] * n
    path = [0]
    visited[0] = True
    start_time = time.time()

    def backtrack(curr, curr_cost):
        nonlocal best_cost, best_path
        if time.time() - start_time > time_limit:
            return
        if len(path) == n:
            total_cost = curr_cost + dist[curr][0]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path[:] + [0]
            return
        for next_city in range(n):
            if not visited[next_city]:
                visited[next_city] = True
                path.append(next_city)
                backtrack(next_city, curr_cost + dist[curr][next_city])
                path.pop()
                visited[next_city] = False

    backtrack(0, 0)
    return best_cost if best_path else None, best_path

# Thuật toán Heuristic Nearest Neighbor
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

    total_cost += dist[path[-1]][path[0]]
    path.append(0)
    return total_cost, path

# Chạy thử và so sánh 2 thuật toán
def run_test(n=15):
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)

    print("\n[Backtracking]")
    print(f"Testing with {n} cities...")
    start_bt = time.time()
    cost_bt, path_bt = tsp_backtracking(dist, time_limit=5)
    end_bt = time.time()
    if path_bt:
        print(f"Time: {end_bt - start_bt:.2f} s")
        print(f"Cost: {cost_bt:.2f}")
        print(f"Path: {path_bt}")
    else:
        print("Không tìm được lời giải trong thời gian giới hạn.")

    print("\n[Nearest Neighbor]")
    print(f"Testing with {n} cities...")
    start_nn = time.time()
    cost_nn, path_nn = tsp_nearest_neighbor(dist)
    end_nn = time.time()
    print(f"Time: {end_nn - start_nn:.2f} s")
    print(f"Cost: {cost_nn:.2f}")
    print(f"Path: {path_nn}")

if __name__ == "__main__":
    run_test(20)  # Bạn có thể đổi thành 6, 10, 20,...

