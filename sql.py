import sqlite3

con = None

def init_db(name):
    con = sqlite3.connect(name + ".db")