import os
import sys
os.chdir("..")
sys.path.append(os.getcwd())
os.chdir(sys.path[0])

import sqlite3
from backend.trader import Trader

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE UserData (username TEXT, name TEXT, cash INTEGER, portfolio TEXT, transaction_history TEXT)")
cursor.execute("INSERT INTO UserData VALUES ('00000000', 'TechBro', 1000000, '{}', '{}')")
cursor.execute("INSERT INTO UserData VALUES ('00000000', 'Tejas', 1000000, '{}', '{}')")
rows = cursor.execute("SELECT id, name, cash, portfolio, transaction_history FROM UserData").fetchall()
print(rows)
cursor.execute("DELETE FROM UserData WHERE name=?", ("Tejas",))
rows = cursor.execute("SELECT id, name, cash, portfolio, transaction_history FROM UserData").fetchall()
print(rows)
