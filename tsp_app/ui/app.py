import tkinter as tk
from tkinter import messagebox
import random
import math
from ui.scrollable_frame import ScrollableFrame
from backtracking.tsp_solver import tsp_backtracking

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver - Backtracking (Time-limited)")

        self.cities = []
        self.dist = []
        self.coord_entries = []
        self.result_text = tk.StringVar()

        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.main_frame = self.scrollable_frame.scrollable_frame

        self.canvas = None
        self.build_main_ui()

    def build_main_ui(self):
        self.cities = []
        self.coord_entries = []
        self.result_text.set("")
        if self.canvas:
            self.canvas.delete("all")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Số thành phố:").grid(row=0, column=0)
        self.city_count_entry = tk.Entry(self.main_frame)
        self.city_count_entry.grid(row=0, column=1)

        tk.Button(self.main_frame, text="Tạo bảng nhập tọa độ", command=self.create_coord_entries).grid(row=0, column=2, padx=5)

        self.coord_frame = tk.Frame(self.main_frame)
        self.coord_frame.grid(row=1, column=0, columnspan=3, pady=5)

        tk.Button(self.main_frame, text="Tọa độ ngẫu nhiên", command=self.random_coords).grid(row=2, column=0, columnspan=3)

        tk.Button(self.main_frame, text="Chạy thuật toán Backtracking", command=self.solve_tsp).grid(row=3, column=0, columnspan=3, pady=5)

        tk.Button(self.main_frame, text="Quay lại", command=self.build_main_ui).grid(row=4, column=0, columnspan=3, pady=5)

        self.result_label = tk.Label(self.main_frame, textvariable=self.result_text, justify="left", fg="blue")
        self.result_label.grid(row=5, column=0, columnspan=3)

        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=3, rowspan=7, padx=10, pady=10)

    def create_coord_entries(self):
        for widget in self.coord_frame.winfo_children():
            widget.destroy()
        self.coord_entries = []

        try:
            n = int(self.city_count_entry.get())
            if n < 2:
                raise ValueError("Phải có ít nhất 2 thành phố")
        except:
            messagebox.showerror("Lỗi", "Nhập số thành phố hợp lệ (>=2)")
            return

        tk.Label(self.coord_frame, text="Thành phố").grid(row=0, column=0)
        tk.Label(self.coord_frame, text="X").grid(row=0, column=1)
        tk.Label(self.coord_frame, text="Y").grid(row=0, column=2)

        for i in range(n):
            tk.Label(self.coord_frame, text=f"{i}").grid(row=i+1, column=0)
            x_entry = tk.Entry(self.coord_frame, width=10)
            y_entry = tk.Entry(self.coord_frame, width=10)
            x_entry.grid(row=i+1, column=1)
            y_entry.grid(row=i+1, column=2)
            self.coord_entries.append((x_entry, y_entry))

    def random_coords(self):
        if not self.coord_entries:
            messagebox.showerror("Lỗi", "Chưa tạo bảng nhập tọa độ")
            return
        for x_entry, y_entry in self.coord_entries:
            x_entry.delete(0, tk.END)
            y_entry.delete(0, tk.END)
            x_entry.insert(0, f"{random.uniform(0,100):.2f}")
            y_entry.insert(0, f"{random.uniform(0,100):.2f}")

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

    def compute_distance_matrix(self):
        n = len(self.cities)
        self.dist = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.dist[i][j] = math.hypot(
                        self.cities[i][0] - self.cities[j][0],
                        self.cities[i][1] - self.cities[j][1]
                    )

    def solve_tsp(self):
        self.cities = self.read_coords()
        if self.cities is None:
            return

        if len(self.cities) > 10:
            messagebox.showwarning(
                "Lưu ý",
                "Thuật toán Backtracking có thể chạy chậm nếu có quá nhiều thành phố.\nSẽ tự động dừng sau 5 giây nếu quá lâu."
            )

        self.compute_distance_matrix()
        cost, path = tsp_backtracking(self.dist, time_limit=5)

        if path is None:
            self.result_text.set("⏱ Không tìm được lời giải trong thời gian giới hạn.")
        else:
            wrapped_path = ""
            for i in range(0, len(path), 5):
              wrapped_path += " -> ".join(map(str, path[i:i+5])) + "\n"

            self.result_text.set(f"Chi phí: {cost:.2f}\nĐường đi:\n{wrapped_path}")
            self.draw_path(path)

    def draw_cities(self):
        self.canvas.delete("all")
        if not self.cities:
            return
        xs = [c[0] for c in self.cities]
        ys = [c[1] for c in self.cities]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        def scale_x(x): return 20 + 360 * (x - min_x) / (max_x - min_x) if max_x > min_x else 200
        def scale_y(y): return 20 + 360 * (y - min_y) / (max_y - min_y) if max_y > min_y else 200

        for i, (x, y) in enumerate(self.cities):
            cx, cy = scale_x(x), scale_y(y)
            self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="red")
            self.canvas.create_text(cx, cy-10, text=str(i), fill="black")

    def draw_path(self, path):
        self.draw_cities()
        if not path or len(path) < 2:
            return
        xs = [self.cities[i][0] for i in path]
        ys = [self.cities[i][1] for i in path]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        def scale_x(x): return 20 + 360 * (x - min_x) / (max_x - min_x) if max_x > min_x else 200
        def scale_y(y): return 20 + 360 * (y - min_y) / (max_y - min_y) if max_y > min_y else 200

        points = []
        for x, y in zip(xs, ys):
            points.append(scale_x(x))
            points.append(scale_y(y))
        self.canvas.create_line(points, fill="blue", width=2, arrow=tk.LAST)
