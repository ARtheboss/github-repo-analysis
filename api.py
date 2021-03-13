'''
MODULE: api
DESC: Perform requests to GitHub API
'''

import requests

def get_commits(owner, name, start, end, page_num = 1):
    ''' Get all commits for repo
    Arguements: str owner - owner of repo; str name - name of repo.
    Returns: Object - json response
    '''

    url = f"https://api.github.com/repos/{owner}/{name}/commits?since={start}&end={end}&per_page=100&page={page_num}"
    res = requests.get(url)

    return res.json()