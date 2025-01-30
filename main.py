import tkinter as tk
from gui import GitControlApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # 设置窗口大小
    app = GitControlApp(root)
    root.mainloop()