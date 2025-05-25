import math
import time

def tsp_backtracking(dist,time_limit=None):
    call_count = 0 # Biến đếm số lần gọi hàm
    cycle_count = 0 # Đếm số chu trình tìm được
    n = len(dist) # Số lượng thành phố
    visited = [False] * n # Danh sách đánh dấu các thành phố đã được thăm
    best_path = [] # Đường đi tốt nhất
    min_cost = math.inf # Chi phí tối thiểu khởi tạo là vô cực
    start_time = time.time() # Thời gian bắt đầu
    def backtrack(curr_pos, count, cost, path):
        nonlocal min_cost, best_path, call_count, cycle_count
        
        call_count += 1 # Đếm số lần gọi hàm backtrack
        
        
        # Kiểm tra thời gian. Nếu vượt quá thời gian quy định, dừng lại
        if time.time() - start_time > time_limit:
            return
        
        # Nếu đã thăm tất cả các thành phố và quay về thành phố đầu tiên
        if count == n and dist[curr_pos][0] > 0: 
            total_cost = cost + dist[curr_pos][0] # Chi phí quay về thành phố đầu tiên
            
            cycle_count += 1  # Tăng số chu trình hợp lệ
            
            # Nếu chi phí nhỏ hơn chi phí tối thiểu hiện tại
            if total_cost < min_cost: 
                min_cost = total_cost # Cập nhật chi phí tối thiểu
                best_path = path + [0] # Cập nhật đường đi tốt nhất
                
                
            return

        # Duyệt qua tất cả các thành phố
        for city in range(n): 
            if not visited[city] and dist[curr_pos][city] > 0: # Nếu chưa thăm thành phố và có đường đi
                visited[city] = True # Đánh dấu thành phố đã thăm
                """ Gọi đệ quy với thành phố tiếp theo 
                thành phố hiện tại là city, 
                tăng số lượng thành phố đã thăm lên 1, 
                chi phí là chi phí hiện tại cộng với chi phí đi từ thành phố hiện tại đến thành phố tiếp theo"""
                backtrack(city, count + 1, cost + dist[curr_pos][city], path + [city])
                visited[city] = False # Đánh dấu lại thành phố chưa thăm để quay lại
    
    # Bắt đầu từ thành phố đầu tiên
    visited[0] = True # Đánh dấu thành phố đầu tiên đã thăm
    """ Gọi hàm backtrack với thành phố hiện tại là 0
    vơi thành phố đầu tiên đã thăm,
    số lượng thành phố đã thăm là 1,
    chi phí là 0 và đường đi là [0]
    """
    backtrack(0, 1, 0, [0]) 
    if not best_path:
        return None, None
    
    return min_cost, best_path, call_count, cycle_count

def get_recommended_time_limit(n):
    """
    Đề xuất thời gian giới hạn phù hợp dựa trên số thành phố
    """
    if n <= 10:
        return 5
    elif n <= 12:
        return 180
    elif n <= 15:
        return 300
    elif n <= 18:
        return 600  # 10 phút 
    else:
        return 900  # 15 phút 