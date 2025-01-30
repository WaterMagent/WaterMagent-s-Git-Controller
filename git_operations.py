from git import Repo
import shutil

def init_repo(repo_path):
    Repo.init(repo_path)
    return f"仓库在 {repo_path} 初始化成功"

def commit_changes(repo_path):
    repo = Repo(repo_path)
    repo.git.add(A=True)
    repo.index.commit("自动提交")
    return "提交完成"

def show_status(repo_path):
    repo = Repo(repo_path)
    status = repo.git.status()
    return status

def push_to_github(repo_path, remote_url):
    repo = Repo(repo_path)
    try:
        origin = repo.remote(name='origin')
    except ValueError:
        origin = repo.create_remote('origin', remote_url)
    origin.push(refspec='{}:{}'.format('master', 'refs/heads/master'))
    return "仓库已上传至GitHub"

def list_local_repos():
    repos = [d for d in os.listdir() if os.path.isdir(os.path.join(d, '.git'))]
    return "\n".join(repos) if repos else "没有找到任何本地仓库"

def delete_repo(repo_path):
    shutil.rmtree(repo_path)
    return "仓库已被删除"