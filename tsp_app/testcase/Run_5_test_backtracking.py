import random
import math
import time

# Thuật toán TSP dùng Backtracking
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

# Hàm test Backtracking với số lượng thành phố lớn
def run_backtracking_test(n=20, time_limit=5):
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)
    
    for i in range(5):  # Lặp lại để kiểm tra nhiều lần
        print("-" * 50)
        print(f"Test #{i + 1}")
        start = time.time()
        cost, path = tsp_backtracking(dist, time_limit)
        end = time.time()

        print(f"Time taken: {end - start:.2f} seconds")
        if path is None:
            print("Không tìm được lời giải trong thời gian giới hạn.")
        else:
            print(f"Chi phí: {cost:.2f}")
            print(f"Đường đi: {path}")

if __name__ == "__main__":
    run_backtracking_test(n=20, time_limit=5)
