# github-repo-analysis

## Features

Use this program to get the following information about a repository during a time interval:
1. Top three most active authors
2. Author with the longest contribution window
3. Heatmap of when commits are occuring

## Execution

Clone the repository.

Make sure the following requirements are met:
* python3
* datetime
* sqlite3
* [requests](https://pypi.org/project/requests/)

To run the program, open a Terminal window and run `main.py` with python3 as such:

```
python3 main.py
```
 
Follow the instructions given by the program.

Note: An interval with more than 6,000 commits will not work as it will exceed the GitHub API's rate limit.
