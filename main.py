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

# User input start/end date in ISO8601 format
start_date = input("Start date (YYYY-MM-DD, default=[start of repo]): ") + "T"
if start_date == "T":
    start_date = date(2008, 1, 1).strftime('%Y-%m-%dT')
end_date = input("End date (YYYY-MM-DD, default=today): ") + "T"
if end_date == "T":
    end_date = datetime.now().strftime('%Y-%m-%dT')

# ensure dates are inclusive
start_date += "00:00:00Z" 
end_date += "23:59:59Z"

#Repeat until valid owner/name combination given
while True:

    # User input to receive valid repo information
    repo_owner = input("Repository Owner (default = apache): ")
    if repo_owner == "":
        repo_owner = "apache"
    repo_name = input("Repository Name (default = hadoop): ")
    if repo_name == "":
        repo_name = "hadoop"

    # test if is valid repository
    commit_obj = test_repo_info(repo_owner, repo_name)

    if 'message' in commit_obj:
        # error in request
        print(commit_obj['message']) 
    else:
        # valid repo information
        break

if init_db(f"{repo_owner}.{repo_name}") == "Created":

    # new db, have to load data

    page_num = 1
    commits_analyzed = 0

    print("\nStarting to access GitHub...")

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
print("\nTop Authors")
for i in range(1, min(4, len(top_authors))):
    print(f"{i}: {top_authors[i-1][0]} - {top_authors[i-1][1]}")



longest_window = get_longest_contribution_window()
print("\nLongest Window:")
print(f"{longest_window[0]} - {longest_window[1].days} days")



heatmap, maxnum = generate_heatmap()

days_of_week = ["M ", "T ", "W ", "Th", "F ", "S ", "Su"]
timings = ["12AM-3AM", "3AM-6AM ", "6AM-9AM ", "9AM-12PM", "12PM-3PM", "3PM-6PM ", "6PM-9PM ", "9PM-12AM"]

TABLE_DATA_MAX_LENGTH = max(2, len(str(maxnum)))
MAX_TIMING_LENGTH = 8

print("\nHeatmap:")

# table header row
header = " " * MAX_TIMING_LENGTH
for day in range(7):
    header += "|" + days_of_week[day] + " " * (TABLE_DATA_MAX_LENGTH - 2)
print(header)

# test of table rows
for row in range(8):

    row_divider = "-" * (MAX_TIMING_LENGTH + (1 + TABLE_DATA_MAX_LENGTH) * 7)
    print(row_divider)

    row_str = timings[row] # row header (timing)
    for column in range(7):
        table_value = str(heatmap[column][row]) 
        row_str += "|" + table_value + " " * (TABLE_DATA_MAX_LENGTH - len(table_value))
    print(row_str)

print("\n")
