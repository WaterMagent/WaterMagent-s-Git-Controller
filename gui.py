import customtkinter as ctk
from tkinter import messagebox, filedialog
from git_operations import init_repo, commit_changes, show_status, push_to_github, list_local_repos, delete_repo
from github_integration import create_github_repo

class GitHubBindingWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.window = ctk.CTkToplevel(master)
        self.window.title("绑定GitHub")
        self.window.geometry("300x150")

        # 创建控件
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.window, text="GitHub 用户名:").place(x=20, y=20)
        self.username_input = ctk.CTkEntry(self.window, width=130)
        self.username_input.place(x=150, y=20)

        ctk.CTkLabel(self.window, text="GitHub 访问令牌:").place(x=20, y=60)
        self.token_input = ctk.CTkEntry(self.window, show="*", width=130)
        self.token_input.place(x=150, y=60)

        ctk.CTkButton(self.window, text="绑定", command=self.bind_github).place(x=80, y=100)

    def bind_github(self):
        self.github_username = self.username_input.get()
        self.github_token = self.token_input.get()
        if self.github_username and self.github_token:
            self.callback(self.github_username, self.github_token)
            self.window.destroy()
        else:
            messagebox.showerror("错误", "请填写GitHub用户名和访问令牌")

class GitControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Git 控制系统")
        self.repo_path = ""
        self.github_token = None
        self.github_username = None
        self.github_repo_name = ""

        # 创建控件
        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(self.master, width=400, height=400)
        frame.pack(fill='both', expand=True)

        row1 = ctk.CTkFrame(frame)
        row1.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkLabel(row1, text="选择Git仓库", anchor='w').pack(side='left', padx=10)
        self.repo_path_label = ctk.CTkLabel(row1, text=self.repo_path, anchor='w')
        self.repo_path_label.pack(side='left', padx=10)

        ctk.CTkButton(row1, text="选择目录", command=self.select_directory).pack(side='right')

        row2 = ctk.CTkFrame(frame)
        row2.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkButton(row2, text="初始化新仓库", command=self.init_repo).pack(side='left', padx=10)
        ctk.CTkButton(row2, text="提交更改", command=self.commit_changes).pack(side='right', padx=10)

        row3 = ctk.CTkFrame(frame)
        row3.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkButton(row3, text="查看状态", command=self.show_status).pack(side='left', padx=10)
        ctk.CTkButton(row3, text="上传到GitHub", command=self.push_to_github).pack(side='right', padx=10)

        row4 = ctk.CTkFrame(frame)
        row4.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkButton(row4, text="列出本地仓库", command=self.list_local_repos).pack(side='left', padx=10)
        ctk.CTkButton(row4, text="删除当前仓库", command=self.delete_repo).pack(side='right', padx=10)

        row5 = ctk.CTkFrame(frame)
        row5.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkButton(row5, text="绑定GitHub", command=self.open_binding_window).pack(side='left', padx=10)

        row6 = ctk.CTkFrame(frame)
        row6.pack(side='top', fill='x', padx=20, pady=10)

        ctk.CTkLabel(row6, text="GitHub 仓库名:", anchor='w').pack(side='left', padx=10)
        self.github_repo_name_input = ctk.CTkEntry(row6, width=130)
        self.github_repo_name_input.pack(side='left', padx=10)

        ctk.CTkButton(row6, text="创建GitHub仓库", command=self.create_github_repo).pack(side='right', padx=10)

    def open_binding_window(self):
        GitHubBindingWindow(self.master, self.set_github_credentials)

    def set_github_credentials(self, username, token):
        self.github_username = username
        self.github_token = token
        print(f"已绑定GitHub用户 {username}")

    def select_directory(self):
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.repo_path = dir_name
            self.repo_path_label.configure(text=dir_name)

    def init_repo(self):
        if not self.repo_path:
            return messagebox.showerror("错误", "请选择或输入有效的仓库路径")
        result = init_repo(self.repo_path)
        messagebox.showinfo("结果", result)

    def commit_changes(self):
        if not self.repo_path:
            return messagebox.showerror("错误", "请选择或输入有效的仓库路径")
        result = commit_changes(self.repo_path)
        messagebox.showinfo("结果", result)

    def show_status(self):
        if not self.repo_path:
            return messagebox.showerror("错误", "请选择或输入有效的仓库路径")
        result = show_status(self.repo_path)
        messagebox.showinfo("仓库状态", result)

    def push_to_github(self):
        if not self.repo_path or not self.github_username or not self.github_token:
            return messagebox.showerror("错误", "请确保选择了仓库路径并绑定了GitHub")
        remote_url = f'https://github.com/{self.github_username}/{self.github_repo_name}.git'
        result = push_to_github(self.repo_path, remote_url)
        messagebox.showinfo("结果", result)

    def list_local_repos(self):
        result = list_local_repos()
        messagebox.showinfo("本地仓库", result)

    def delete_repo(self):
        if not self.repo_path:
            return messagebox.showerror("错误", "请选择或输入有效的仓库路径")
        result = delete_repo(self.repo_path)
        messagebox.showinfo("结果", result)

    def create_github_repo(self):
        if not self.github_username or not self.github_repo_name:
            return messagebox.showerror("错误", "请填写GitHub用户名和仓库名")
        result = create_github_repo(self.github_token, self.github_username, self.github_repo_name)
        messagebox.showinfo("结果", result)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x400")  # 设置窗口大小
    app = GitControlApp(root)
    root.mainloop()