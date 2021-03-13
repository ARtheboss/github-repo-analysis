import requests

def get_commits(name, owner):

    res = requests.get(f"https://api.github.com/repos/{owner}/{name}/commits")

    print(res.json())