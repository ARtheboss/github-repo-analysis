'''
MODULE: api
DESC: Handle queries to SQL Database
'''

import sqlite3
from datetime import datetime, timedelta
from random import getrandbits


con = None

def init_db(name):

    global con

    con = sqlite3.connect(name + ".db")

    cur = con.cursor()

    if cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'Commits'").fetchone() != None:
        
        overwrite = input("Previous data for this repo found. Overwrite? (Y/default = N): ")
        if overwrite.upper() == "Y":
            # clean old tables
            cur.execute("DROP TABLE Commits")
            cur.execute("DROP TABLE Authors")
        else:
            print("Note: New date range may be larger than old date range")
            return "Reused"
        

    # new db
    cur.execute("CREATE TABLE Authors (author_id varchar(255), login varchar(255), commits int(255),  PRIMARY KEY (author_id))")
    cur.execute("CREATE TABLE Commits (node_id varchar(255), date datetime, message varchar(1023), author_id varchar(255), PRIMARY KEY (node_id), FOREIGN KEY (author_id) REFERENCES Authors(author_id))")
    
    con.commit()

    return "Created"


def add_commits_to_db(json):
    
    cur = con.cursor()

    for commit in json:
        try:
            node_id = commit['node_id']
        except:
            print(json)
        date = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
        message = commit['commit']['message']
        #verified = str(commit['commit']['verification']['verified']).upper()

        if commit['author'] == None:
            author_info_loc = 'committer'
        else:
            author_info_loc = 'author'

        try:
            author_id = commit[author_info_loc]['node_id']
            author_login = commit[author_info_loc]['login']
        except:
            author_id = getrandbits(20)
            if commit['commit']['author'] == None:
                author_login = commit['commit']['committer']['name']
            else:
                author_login = commit['commit']['author']['name']

        resp = cur.execute("SELECT commits FROM Authors WHERE author_id = ?", (author_id, )).fetchone()

        if resp != None:
            new_commits = resp[0] + 1
            cur.execute("UPDATE Authors SET commits = ? WHERE author_id = ?", (new_commits, author_id))
        else:
            cur.execute("INSERT INTO Authors VALUES (?,?,1)", (author_id, author_login))

        args = (node_id, date.strftime('%Y-%m-%d %H:%M:%S'), message, author_id)
        cur.execute("INSERT INTO Commits VALUES (?, ?, ?, ?)", args)

        con.commit()

def get_top_authors():

    cur = con.cursor()
    
    return cur.execute("SELECT * FROM Authors ORDER BY commits DESC").fetchall()


def get_longest_contribution_window():

    cur = con.cursor()
    
    authors = cur.execute("SELECT login, author_id FROM Authors").fetchall()

    longest_range = timedelta(days = 0)
    author_with_longest_window = "No authors"

    for (login, author_id) in authors:

        first_commit = cur.execute("SELECT date FROM Commits WHERE author_id = ? ORDER BY date ASC", (author_id, )).fetchone()
        last_commit = cur.execute("SELECT date FROM Commits WHERE author_id = ? ORDER BY date DESC", (author_id, )).fetchone()

        if first_commit == None:
            continue
        else:
            first_commit = datetime.strptime(first_commit[0],'%Y-%m-%d %H:%M:%S')
            last_commit = datetime.strptime(last_commit[0],'%Y-%m-%d %H:%M:%S')

        if last_commit - first_commit > longest_range:
            author_with_longest_window = login
            longest_range = last_commit - first_commit

    return (author_with_longest_window, longest_range)

def generate_heatmap():

    cur = con.cursor()

    heatmap = []
    for i in range(7):
        heatmap.append([0] * 8)

    commits = cur.execute("SELECT date FROM Commits").fetchall()

    maxval = 0

    for date in commits:

        date = datetime.strptime(date[0],'%Y-%m-%d %H:%M:%S')

        day_of_week = date.weekday()
        hour = date.hour
        three_hour_range = hour // 3

        heatmap[day_of_week][three_hour_range] += 1
        maxval = max(maxval, heatmap[day_of_week][three_hour_range])

    return (heatmap, maxval)


