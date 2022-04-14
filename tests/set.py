import os
import sys
os.chdir("..")
sys.path.append(os.getcwd())
from utils.utils import printall
import sqlite3
from contextlib import closing

"""with closing(sqlite3.connect(f"{os.getcwd()}/backend/maindb/data.db", isolation_level=None)) as connection:
    with closing(connection.cursor()) as cursor:
        cursor.execute(
        "DELETE from users WHERE id = ?",
        ("tanujks", )
        )"""

printall(f"{os.getcwd()}/backend/maindb/tokens.db", 'tokens')
print("\n")
printall(f"{os.getcwd()}/backend/maindb/data.db", 'users')
print("\n")
printall(f"{os.getcwd()}/backend/maindb/user_data.db", 'UserData')
