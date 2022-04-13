import sqlite3
import os

connection = sqlite3.connect(f"{os,getcwd()}/auth/maindb/data.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
