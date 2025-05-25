import os
import time
import glob
from typing import List, Optional

from backtracking.tsp_solver import tsp_backtracking, get_recommended_time_limit


# Hàm đọc ma trận từ file .txt
def load_matrix_from_file(filepath: str) -> List[List[int]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            matrix = []
            for line in file:
                line = line.strip()
                if line:  # Bỏ qua dòng trống
                    row = list(map(int, line.split()))
                    matrix.append(row)
        return matrix
    except FileNotFoundError:
        print(f"Không tìm thấy file: {filepath}")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return None

# Hàm tính số chu trình lý thuyết tối đa cho TSP
def calculate_theoretical_cycles(n: int) -> int:
    """
    Tính số chu trình lý thuyết tối đa cho TSP với n thành phố
    Với TSP có hướng: (n-1)!
    """
    if n <= 1:
        return 0
    
    factorial = 1
    for i in range(1, n):
        factorial *= i
    
    return factorial

# Định dạng đường đi 
def format_path(path: List[int]) -> str:
    if not path:
        return "Không có đường đi"
    
    formatted_path = [str(city) for city in path]
    return " -> ".join(formatted_path)

# Kiểm tra tính hợp lệ của ma trận
def validate_matrix(matrix: List[List[int]]) -> bool:
    """Kiểm tra tính hợp lệ của ma trận"""
    if not matrix:
        return False
    
    n = len(matrix)
    
    # Kiểm tra ma trận vuông
    for row in matrix:
        if len(row) != n:
            return False
    
    # Kiểm tra đường chéo chính = 0
    for i in range(n):
        if matrix[i][i] != 0:
            print(f"Cảnh báo: Phần tử trên đường chéo chính [{i}][{i}] = {matrix[i][i]} != 0")
    
    return True

def run_single_test(matrix_file: str, time_limit: Optional[int] = None) -> dict:

    print(f"\n{'='*60}")
    print(f"CHẠY TEST TSP BACKTRACKING")
    
    # Đọc ma trận từ file
    matrix = load_matrix_from_file(matrix_file)
    if matrix is None:
        return {"error": "Không thể đọc ma trận từ file"}
    
    # Kiểm tra ma trận
    if not validate_matrix(matrix):
        return {"error": "Ma trận không hợp lệ"}
    
    n = len(matrix)
    print(f"Kích thước ma trận: {n}x{n}")
    
     # Hiển thị ma trận
    print(f"\nMa trận khoảng cách:")
    print("    ", end="")
    for j in range(n):
        print(f"{j+1:4}", end="")
    print()
    
    for i in range(n):
        print(f"{i+1:2}: ", end="")
        for j in range(n):
            print(f"{matrix[i][j]:4}", end="")
        print()
    # Chạy thuật toán
    print(f"\nBắt đầu chạy thuật toán TSP Backtracking...")
    
    # Xác định thời gian giới hạn
    if time_limit is None:
        time_limit = get_recommended_time_limit(n)
    
    # Tính số chu trình lý thuyết
    theoretical_cycles = calculate_theoretical_cycles(n)
    
    # Ghi lại thời gian bắt đầu
    start_time = time.time()
    
    try:
        result = tsp_backtracking(matrix, time_limit)
        
        # Thời gian kết thúc
        end_time = time.time()
        execution_time = end_time - start_time
        
        if len(result) == 4:
            optimal_cost, optimal_path, recursion_calls, valid_cycles = result
        else:
            # Trường hợp không tìm thấy giải pháp
            optimal_cost, optimal_path = result
            recursion_calls, valid_cycles = 0, 0
        
    except Exception as e:
        return {"error": f"Lỗi khi chạy thuật toán: {e}"}
    
    # Hiển thị kết quả cơ bản
    print(f"\n{'='*40}")
    print(f"KẾT QUẢ")
    print(f"{'='*40}")
    
    print(f"Chi phí tối ưu: {optimal_cost}")
    
    # Hiển thị đường đi tối ưu
    if optimal_path:
        formatted_path = format_path(optimal_path)
        print(f"Đường đi tối ưu: {formatted_path}")
    else:
        print("Đường đi tối ưu: Không tìm thấy")
    
    print(f"Số lần gọi đệ quy: {recursion_calls:,}")
    print(f"Chu trình hợp lệ tìm được: {valid_cycles:,}")
    print(f"Chu trình lý thuyết: {theoretical_cycles:,}")
    print(f"Thời gian thực thi: {execution_time:.4f}s")
    print(f"Thời gian giới hạn: {time_limit}s")
    
    # Tạo kết quả trả về
    result_dict = {
        "matrix_size": f"{n}x{n}",
        "optimal_cost": optimal_cost,
        "optimal_path": optimal_path,
        "formatted_path": format_path(optimal_path) if optimal_path else "Không tìm thấy",
        "recursion_calls": recursion_calls,
        "valid_cycles_found": valid_cycles,
        "theoretical_cycles": theoretical_cycles,
        "execution_time": execution_time,
        "time_limit": time_limit
    }
    
    return result_dict

def run_all_tests(test_directory=None):
    """Chạy test cho tất cả file txt trong thư mục testcase"""
    # Tự động xác định thư mục testcase
    if test_directory is None:
        
        # Lấy thư mục chứa file hiện tại (test_runner.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_directory = current_dir
    
    print("BẮT ĐẦU KIỂM TRA THUẬT TOÁN TSP BACKTRACKING")
    print("="*60)
    
    # Tìm tất cả file .txt trong thư mục testcase
    if not os.path.exists(test_directory):
        print(f"Thư mục {test_directory} không tồn tại!")
        return []
    
    txt_files = glob.glob(os.path.join(test_directory, "*.txt"))
    
    if not txt_files:
        print(f"Không tìm thấy file .txt nào trong thư mục {test_directory}")
        return []
    
    # Sắp xếp file theo tên (matrix_4x4, matrix_6x6, matrix_10x10)
    txt_files.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x)))))
    
    results = []
    total_start_time = time.time()
    
    # Chạy test cho từng file
    for filename in txt_files:
        result = run_single_test(filename)
        if result and "error" not in result:
            results.append(result)
    
    total_time = time.time() - total_start_time
    
    # Tổng kết đơn giản
    print(f"\n{'='*40}")
    print("TỔNG KẾT")
    print(f"{'='*40}")
    print(f"Tổng số test: {len(results)}")
    print(f"Tổng thời gian: {total_time:.2f}s")
    
    # Hiển thị tóm tắt kết quả các test
    if results:
        print(f"\nTÓM TẮT KẾT QUẢ:")
        print(f"{'Ma trận':<12} {'Chi phí':<10} {'Đường đi tối ưu':<25} {'Thời gian':<12}")
        print("-" * 65)
        for result in results:
            matrix_size = result['matrix_size']
            optimal_cost = result['optimal_cost']
            formatted_path = result['formatted_path']
            execution_time = f"{result['execution_time']:.3f}s"
            
            # Cắt ngắn đường đi nếu quá dài
            if len(formatted_path) > 22:
                formatted_path = formatted_path[:19] + "..."
            
            print(f"{matrix_size:<12} {optimal_cost:<10} {formatted_path:<25} {execution_time:<12}")
    
    return results