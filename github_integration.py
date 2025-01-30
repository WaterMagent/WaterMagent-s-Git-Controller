import requests

def create_github_repo(github_token, username, repo_name):
    url = 'https://api.github.com/user/repos'
    headers = {'Authorization': f'token {github_token}'}
    data = {'name': repo_name}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return "GitHub仓库创建成功"
    else:
        return f"创建失败: {response.json().get('message')}"