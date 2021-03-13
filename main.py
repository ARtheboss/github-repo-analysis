'''
Main file
Run in terminal 'python3 main.py' to use project
Dependencies:
 - sqlite3
 - requests
'''

from api import *
from sql import *
from datetime import date, datetime

start_date = input("Start date (YYYY-MM-DD, default=[start of repo]): ") + "T"
if start_date == "T":
    start_date = date(2008, 1, 1).strftime('%Y-%m-%dT')
end_date = input("Start date (YYYY-MM-DD, default=today): ") + "T"
if end_date == "T":
    end_date = datetime.now().strftime('%Y-%m-%dT')

start_date += "00:00:00Z"
end_date += "23:59:59Z"

#Repeat until valid owner/name combination given
while True:

    # User input to recieve problem inputs
    repo_owner = input("Repository Owner (default = apache): ")
    if repo_owner == "":
        repo_owner = "apache"
    repo_name = input("Repository Name (default = hadoop): ")
    if repo_name == "":
        repo_name = "hadoop"

    break

    commit_obj = get_commits(repo_owner, repo_name, start_date, end_date)

    if 'message' in commit_obj:
        print(commit_obj['message'])
    else:
        break

if init_db(f"{repo_owner}.{repo_name}") == "Created":


    page_num = 1
    commits_analyzed = 0
    print("Starting to access GitHub...")
    while len(commit_obj) > 0:
        commit_obj = get_commits(repo_owner, repo_name, start_date, end_date, page_num)
        if 'message' in commit_obj:
            print(commit_obj['message'])
            break
        add_commits_to_db(commit_obj)
        commits_analyzed += len(commit_obj)
        print(f"{commits_analyzed} commits analyzed", end="\r")
        page_num += 1

    print(f"{commits_analyzed} commits analyzed")

top_authors = get_top_authors()
print("Top Authors")
for i in range(1, 4):
    print(f"{i}: {top_authors[i-1][1]} - {top_authors[i-1][2]}")

longest_window = get_longest_contribution_window()
print("\nLongest Window:")
print(f"{longest_window[0]} - {longest_window[1].days} days")

heatmap, maxnum = generate_heatmap()

max_width = max(2, maxnum // 10 + 1)

days_of_week = ["M ", "T ", "W ", "Th", "F ", "S ", "Su"]

timings = ["12AM-3AM", "3AM-6AM ", "6AM-9AM ", "9AM-12PM", "12PM-3PM", "3PM-6PM ", "6PM-9PM ", "9PM-12AM"]

MAX_TIMING_LENGTH = 8

print("\nHeatmap:")

header = " " * MAX_TIMING_LENGTH
for day in range(7):
    header += "|" + days_of_week[day] + " " * (max_width - 2)

print(header)


for row in range(8):
    row_divider = "-" * (MAX_TIMING_LENGTH + (1 + max_width) * 7)
    print(row_divider)
    row_str = timings[row]
    for column in range(7):
        row_str += "|" + str(heatmap[column][row]) + " " * (max_width - heatmap[column][row] // 10 - 1)
    print(row_str)

print("\n")
