import tkinter as tk
from ui.app import TSPApp
from testcase.test_runner import run_all_tests


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()
    
    # print("TSP BACKTRACKING TEST SUITE")
    # print("="*40)
    # # Chạy nhiều test cases
    # results = run_all_tests()
    
