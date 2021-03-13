from api import *
from sql import *

repo_name = input("Repository Name: ")
repo_owner = input("Repository Owner: ")

get_commits(repo_name, repo_owner)