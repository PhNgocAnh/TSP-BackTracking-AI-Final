import math
import time


def tsp_backtracking(dist,time_limit=5):
    call_count = 0 # Biến đếm số lần gọi hàm
    n = len(dist)
    visited = [False] * n
    best_path = []
    min_cost = math.inf
    start_time = time.time()
    
    def backtrack(curr_pos, count, cost, path):
        nonlocal min_cost, best_path, call_count
        
        call_count += 1 # Đếm số lần gọi hàm
        
        # Kiểm tra thời gian. Nếu vượt quá thời gian quy định, dừng lại
        if time.time() - start_time > time_limit:
            return
        
        if count == n and dist[curr_pos][0] > 0:
            total_cost = cost + dist[curr_pos][0]
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = path + [0]
            return

        for city in range(n):
            if not visited[city] and dist[curr_pos][city] > 0:
                visited[city] = True
                backtrack(city, count + 1, cost + dist[curr_pos][city], path + [city])
                visited[city] = False
    
    # Bắt đầu từ thành phố đầu tiên
    visited[0] = True
    backtrack(0, 1, 0, [0])

    if not best_path:
        return None, None
    return min_cost, best_path, call_count 
