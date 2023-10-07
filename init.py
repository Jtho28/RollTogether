#/bin/python3
import rtArch
from rtArch import init
import sqlite3

init()

db = sqlite3.connect('./instance/rollt.db')
cursor=db.cursor()


with open('./instance/db_test_dat.sql') as file:
  query = (file.read())
  cursor.executescript(query)
