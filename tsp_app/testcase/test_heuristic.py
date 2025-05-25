import random
import math
import time

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

def generate_cities(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

def compute_distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.hypot(cities[i][0] - cities[j][0], cities[i][1] - cities[j][1])
    return dist

def run_test(n=20):
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)
    print(f"Testing with {n} cities...")
    start = time.time()
    cost, path = tsp_backtracking(dist, time_limit=5)
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
    if path is None:
        print("Không tìm được lời giải trong thời gian giới hạn.")
    else:
        print(f"Chi phí: {cost:.2f}")
        print(f"Đường đi: {path}")





if __name__ == "__main__":
    run_test()
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

    total_cost += dist[path[-1]][path[0]]  # Trở về điểm xuất phát
    path.append(0)
    return total_cost, path

def run_test(n=20):
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)
    print(f"Testing with {n} cities...")
    start = time.time()
    
    if n <= 15:
        cost, path = tsp_backtracking(dist, time_limit=5)
    else:
        cost, path = tsp_nearest_neighbor(dist)
    
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
    if path is None:
        print("Không tìm được lời giải trong thời gian giới hạn.")
    else:
        print(f"Chi phí: {cost:.2f}")
        print(f"Đường đi: {path}")

if __name__ == "__main__":
    run_test(20)
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
                print(f"New best cost: {best_cost:.2f} at time {time.time() - start_time:.2f}s")
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
