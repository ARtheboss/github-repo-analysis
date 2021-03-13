'''
MODULE: api
DESC: Perform requests to GitHub API
'''

import requests

def test_repo_info(owner, name):
    ''' Check if repo exists
    Arguements: String owner - owner of repo; String name - name of repo.
    Returns: Object - json response
    '''

    url = f"https://api.github.com/repos/{owner}/{name}/commits?per_page=1"
    res = requests.get(url)

    return res.json()

def get_commits(owner, name, start, end, page_num = 1):
    ''' Get 100 (max) commits for repo
    Arguements: String owner - owner of repo; String name - name of repo; Int page_num - which 100 commits
    Returns: Object - json response
    '''

    url = f"https://api.github.com/repos/{owner}/{name}/commits?since={start}&end={end}&per_page=100&page={page_num}"
    res = requests.get(url)

    return res.json()