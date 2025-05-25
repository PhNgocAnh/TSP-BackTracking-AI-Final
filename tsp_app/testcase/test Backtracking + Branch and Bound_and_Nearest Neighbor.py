import random
import math
import time

# Tạo danh sách thành phố với tọa độ ngẫu nhiên
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

# Backtracking + Branch & Bound
def tsp_backtracking_branch_and_bound(dist, time_limit=5):
    n = len(dist)
    best_cost = float('inf')
    best_path = None
    visited = [False] * n
    path = [0]
    visited[0] = True
    start_time = time.time()
    call_count = 0

    def backtrack(curr, curr_cost):
        nonlocal best_cost, best_path, call_count
        call_count += 1
        if time.time() - start_time > time_limit:
            return
        if curr_cost >= best_cost:
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

    start = time.time()
    backtrack(0, 0)
    end = time.time()
    return best_cost if best_path else None, best_path, end - start, call_count

# Nearest Neighbor heuristic
def tsp_nearest_neighbor(dist):
    n = len(dist)
    visited = [False] * n
    path = [0]
    visited[0] = True
    cost = 0
    curr = 0

    start = time.time()
    for _ in range(n - 1):
        next_city = min(
            (j for j in range(n) if not visited[j]),
            key=lambda j: dist[curr][j]
        )
        visited[next_city] = True
        cost += dist[curr][next_city]
        path.append(next_city)
        curr = next_city
    cost += dist[curr][0]
    path.append(0)
    end = time.time()
    return cost, path, end - start

# Hàm chạy so sánh
def run_compare(n=20):
    print(f"\n=== SO SÁNH VỚI {n} THÀNH PHỐ ===")
    cities = generate_cities(n)
    dist = compute_distance_matrix(cities)

    # Backtracking
    print("\n[1] Backtracking + Branch & Bound (time_limit = 5s):")
    cost_bt, path_bt, time_bt, calls = tsp_backtracking_branch_and_bound(dist, time_limit=5)
    if path_bt:
        print(f"→ Chi phí: {cost_bt:.2f}")
        print(f"→ Thời gian: {time_bt:.2f} giây")
        print(f"→ Số lần gọi đệ quy: {calls}")
    else:
        print("→ Không tìm được lời giải trong thời gian giới hạn.")

    # Nearest Neighbor
    print("\n[2] Nearest Neighbor (Heuristic):")
    cost_nn, path_nn, time_nn = tsp_nearest_neighbor(dist)
    print(f"→ Chi phí: {cost_nn:.2f}")
    print(f"→ Thời gian: {time_nn:.4f} giây")
    print(f"→ Không dùng đệ quy.")

# Chạy thử
if __name__ == "__main__":
    run_compare(n=20)
