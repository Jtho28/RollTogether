#/bin/python3
import sqlite3


db = sqlite3.connect('./instance/rollt.db')
cursor=db.cursor()


with open('./instance/db_test_dat.sql') as file:
  query = (file.read())
  cursor.executescript(query)
