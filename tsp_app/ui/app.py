import tkinter as tk
from tkinter import messagebox, ttk
import random
from scipy.spatial.distance import cdist
import time
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


from backtracking.tsp_solver import tsp_backtracking
from backtracking.tsp_solver import get_recommended_time_limit
# from backtracking_with_bound.tsp_backtracking_bound import tsp_backtracking_with_bound

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver")
        self.root.geometry("1200x700")

        self.cities = [] 
        self.dist = []
        self.coord_entries = []
        self.result_text = tk.StringVar() 

        self.setup_ui()
    
    # Hàm thiết lập giao diện người dùng
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel for controls
        left_panel = tk.Frame(main_container, width=400)
        left_panel.pack(side="left", fill="y", padx=(0, 15))
        left_panel.pack_propagate(False)

        # Right panel for graphs
        right_panel = tk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

    # Hàm thiết lập giao diện cho bảng điều khiển bên trái
    def setup_left_panel(self, parent):
        # Input section
        input_frame = tk.LabelFrame(parent, text="Cài đặt", font=("Arial", 14, "bold"))
        input_frame.pack(fill="x", pady=(0, 10))

        tk.Label(input_frame, text="Số thành phố:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.city_count_entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
        self.city_count_entry.grid(row=0, column=1, padx=5, pady=8)

        tk.Button(input_frame, text="Tạo bảng tọa độ", 
                 command=self.create_coord_entries, 
                 relief="raised", bd=2, font=("Arial", 12, "bold"),
                 height=2, width=15).grid(row=0, column=2, padx=5, pady=8)

        # Coordinates section
        self.coord_frame = tk.LabelFrame(parent, text="Tọa độ thành phố", font=("Arial", 14, "bold"))
        self.coord_frame.pack(fill="x", pady=(0, 10))

        # Scrollable frame for coordinates
        canvas = tk.Canvas(self.coord_frame, height=150)
        scrollbar = ttk.Scrollbar(self.coord_frame, orient="vertical", command=canvas.yview)
        self.scrollable_coord_frame = tk.Frame(canvas)

        self.scrollable_coord_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_coord_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        action_frame = tk.Frame(parent)
        action_frame.pack(fill="x", pady=(0, 10))

        tk.Button(action_frame, text="Tọa độ ngẫu nhiên", 
                 command=self.random_coords, 
                 relief="raised", bd=2, font=("Arial", 12, "bold"),
                 height=2).pack(fill="x", pady=3)
        
        tk.Button(action_frame, text="Chạy thuật toán Backtracking", 
                 command=self.solve_tsp, 
                 relief="raised", bd=2, font=("Arial", 12, "bold"),
                 height=2).pack(fill="x", pady=3)
        
        tk.Button(action_frame, text="Làm mới", 
                 command=self.reset_all, 
                 relief="raised", bd=2, font=("Arial", 12, "bold"),
                 height=2).pack(fill="x", pady=3)

        # Results section
        result_frame = tk.LabelFrame(parent, text="Kết quả", font=("Arial", 14, "bold"))
        result_frame.pack(fill="both", expand=True)

        # Text widget for better result display
        self.result_text_widget = tk.Text(result_frame, height=15, font=("Arial", 16, "bold"))
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text_widget.yview)
        self.result_text_widget.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text_widget.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")

    # Hàm thiết lập giao diện cho bảng bên phải => # Hiển thị đồ thị và kết quả
    def setup_right_panel(self, parent):
        # Create matplotlib figure with subplots
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax1 = self.fig.add_subplot(211)  # Đồ thị TSP
        self.ax2 = self.fig.add_subplot(212)  # Đường đi tối ưu
        
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas for matplotlib
        self.canvas_matplotlib = FigureCanvasTkAgg(self.fig, parent)
        self.canvas_matplotlib.draw()
        self.canvas_matplotlib.get_tk_widget().pack(fill="both", expand=True)

        # Initial empty plots
        self.ax1.set_title("Đồ thị TSP ", fontsize=14, fontweight='bold')
        self.ax2.set_title("Đường đi tối ưu", fontsize=12, fontweight='bold')
        self.ax1.axis('off')
        self.ax2.axis('off')

    # Hàm tạo bảng nhập tọa độ
    def create_coord_entries(self):
        # Clear existing entries
        for widget in self.scrollable_coord_frame.winfo_children():
            widget.destroy()
        self.coord_entries = []

        try:
            n = int(self.city_count_entry.get())
            if n < 2:
                raise ValueError("Phải có ít nhất 2 thành phố")
        except:
            messagebox.showerror("Lỗi", "Nhập số thành phố hợp lệ (>=2)")
            return

        # Headers
        tk.Label(self.scrollable_coord_frame, text="Thành phố", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=3)
        tk.Label(self.scrollable_coord_frame, text="X", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=3)
        tk.Label(self.scrollable_coord_frame, text="Y", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=3)

        # Create entry fields
        for i in range(n):
            tk.Label(self.scrollable_coord_frame, text=f"{i}", font=("Arial", 11)).grid(row=i+1, column=0, padx=5, pady=3)
            x_entry = tk.Entry(self.scrollable_coord_frame, width=8, font=("Arial", 11))
            y_entry = tk.Entry(self.scrollable_coord_frame, width=8, font=("Arial", 11))
            x_entry.grid(row=i+1, column=1, padx=5, pady=3)
            y_entry.grid(row=i+1, column=2, padx=5, pady=3)
            self.coord_entries.append((x_entry, y_entry))

    # Hàm tạo tọa độ ngẫu nhiên
    def random_coords(self):
        if not self.coord_entries:
            messagebox.showerror("Lỗi", "Chưa tạo bảng nhập tọa độ")
            return
        
        for x_entry, y_entry in self.coord_entries:
            x_entry.delete(0, tk.END)
            y_entry.delete(0, tk.END)
            x_entry.insert(0, str(random.randint(50, 100)))
            y_entry.insert(0, str(random.randint(50, 100)))
        
        # Update the original graph
        coords = self.read_coords() # Đọc tọa độ từ các ô nhập
        if coords:
            self.cities = coords
            self.compute_distance_matrix() # Tính toán ma trận khoảng cách
            self.draw_original_graph() # Vẽ lại đồ thị

    # Hàm đọc tọa độ từ các ô nhập
    def read_coords(self):
        coords = []
        for i, (x_entry, y_entry) in enumerate(self.coord_entries):
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                coords.append((x, y))
            except:
                messagebox.showerror("Lỗi", f"Tọa độ thành phố {i} không hợp lệ")
                return None
        return coords

    # Hàm tính toán ma trận khoảng cách. Sử dụng scipy để tính toán khoảng cách Euclidean
    def compute_distance_matrix(self):
        if len(self.cities) > 0:
            self.dist = cdist(self.cities, self.cities, metric='euclidean')

    # Hàm vẽ đồ thị TSP ban đầu => Sử dụng NetworkX và matplotlib để vẽ đồ thị => Nối các thành phố với nhau
    def draw_original_graph(self):

        self.ax1.clear()
        
        if not self.cities:
            self.ax1.set_title("Đồ thị TSP ", fontsize=12, fontweight='bold')
            self.ax1.axis('off')
            self.canvas_matplotlib.draw()
            return

        # Create complete graph
        G = nx.complete_graph(len(self.cities))
        
        # Set positions based on coordinates
        pos = {i: self.cities[i] for i in range(len(self.cities))}
        
        # Draw the graph
        nx.draw(G, pos, ax=self.ax1, 
                node_color='lightcoral', 
                node_size=350,
                with_labels=True,
                font_size=10,
                font_weight='bold',
                edge_color='black',
                alpha=0.7)
        
        self.ax1.set_title("Đồ thị TSP ", fontsize=12, fontweight='bold')
        self.ax1.axis('equal')
        
        self.canvas_matplotlib.draw()

    # Hàm vẽ đường đi tối ưu => Sử dụng NetworkX và matplotlib để vẽ đường đi tối ưu 
    def draw_solution_path(self, path):
        self.ax2.clear()
        
        if not path or not self.cities:
            self.ax2.set_title("Đường đi tối ưu", fontsize=12, fontweight='bold')
            self.ax2.axis('off')
            self.canvas_matplotlib.draw()
            return

        # Create directed graph for the path with arrows
        G = nx.DiGraph()  # Changed to directed graph
        G.add_nodes_from(range(len(self.cities)))
        
        # Add edges for the path
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1])
        
        # Set positions
        pos = {i: self.cities[i] for i in range(len(self.cities))}
        
        # Draw all nodes
        nx.draw_networkx_nodes(G, pos, ax=self.ax2,
                              node_color='lightgreen',
                              node_size=350,  
                              edgecolors='darkgreen',
                              linewidths=2)
        
        # Draw the path edges with arrows
        nx.draw_networkx_edges(G, pos, ax=self.ax2,
                              edge_color='red',
                              width=3,  # Thicker arrows
                              alpha=0.8,
                              arrows=True,
                              arrowsize=25,  # Larger arrow heads
                              arrowstyle='->')
        
        # Draw labels with larger font
        nx.draw_networkx_labels(G, pos, ax=self.ax2,
                               font_size=12,  
                               font_weight='bold',
                               font_color='white')
        
        self.ax2.set_title(" Chu trình tối ưu ", fontsize=14, fontweight='bold')
        self.ax2.axis('equal')
        
        self.canvas_matplotlib.draw()

    def solve_tsp(self):
        self.cities = self.read_coords()
        n = len(self.cities)
        
        if self.cities is None:
            return
        
        time_limit = get_recommended_time_limit(n) # Lấy thời gian giới hạn khuyến nghị

        if n > 10:
            # Hỏi người dùng có muốn tiếp tục không
            result = messagebox.askyesno(
                "Cảnh báo",
                f"Với {n} thành phố, thuật toán có thể chạy rất lâu ({time_limit}s).\n"
                "Bạn có muốn tiếp tục không?"
            )
            if not result:
                return

        self.compute_distance_matrix() # Tính toán ma trận khoảng cách
        self.draw_original_graph() # Nối các thành phố với nhau
        
        # Clear previous results
        self.result_text_widget.delete(1.0, tk.END)
        self.result_text_widget.insert(tk.END, "Đang tính toán...\n")
        self.root.update()

        start_time = time.time() # Thời gian bắt đầu
        
        try:
            cost, path, call_count, cycle_count = tsp_backtracking(self.dist,time_limit)
        except Exception as e:
            self.result_text_widget.delete(1.0, tk.END) # 
            self.result_text_widget.insert(tk.END, f"Lỗi: {str(e)}")
            return
        
        end_time = time.time() # Thời gian kết thúc

        # Clear and update results
        self.result_text_widget.delete(1.0, tk.END)
        
        if path is None:
            self.result_text_widget.insert(tk.END, "⏱ Không tìm được lời giải trong thời gian giới hạn.\n")
        else:
            # Format path display with arrows
            wrapped_path = ""
            for i in range(0, len(path), 6):  # Reduced from 8 to 6 for better display
                line_cities = path[i:i+6]
                if i == 0:
                    # First line - add starting arrow
                    wrapped_path += " " + " ➜ ".join(map(str, line_cities))
                else:
                    wrapped_path += "   " + " ➜ ".join(map(str, line_cities))
                
                # Add newline if not the last segment
                if i + 6 < len(path):
                    wrapped_path += " ➜\n"
                else:
                    # Last line - add return arrow to start
                    if len(path) > 1 and path[-1] != path[0] :
                        wrapped_path += f" ➜ {path[0]} "

            result_text = f"""════════════ KẾT QUẢ ════════════

Chi phí tối ưu: {cost:.2f}

Chu trình tối ưu:
{wrapped_path}

Thời gian thực thi: {round(end_time - start_time, 4)} giây
Số lần gọi đệ quy: {call_count:,}
Số chu trình hợp lệ tìm được: {cycle_count:,}
═══════════════════════════════

"""
            
            self.result_text_widget.insert(tk.END, result_text)
            self.draw_solution_path(path)

    def reset_all(self):
        """Reset everything to initial state"""
        self.cities = []
        self.dist = []
        self.coord_entries = []
        
        # Clear coordinate entries
        for widget in self.scrollable_coord_frame.winfo_children():
            widget.destroy()
        
        # Clear city count
        self.city_count_entry.delete(0, tk.END)
        
        # Clear results
        self.result_text_widget.delete(1.0, tk.END)
        
        # Clear graphs
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title("Đồ thị TSP ", fontsize=12, fontweight='bold')
        self.ax2.set_title("Đường đi tối ưu", fontsize=12, fontweight='bold')
        self.ax1.axis('off')
        self.ax2.axis('off')
        self.canvas_matplotlib.draw()
