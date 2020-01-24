# This file is only used to create 24 hours of test data in mariadb.OpenHAB.test

import mysql.connector as mariadb
import random
import sys

if(len(sys.argv) != 4):
	sys.exit("Incorrect number of arguments. Usage: [HOST] [USER] [PASSWORD]\nClosing...")	

# Connect to local mariadb server
db = mariadb.connect(
    host=sys.argv[1],
    user=sys.argv[2],
    passwd=sys.argv[3],
    database="test"
)

cur = db.cursor()

date = "2020-01-21"
h = 0
m = 0

while(h < 24):
	m = 0
	while(m < 60):
		# print("INSERT INTO test (Time, Value) VALUES ('" + date + " " + str(h) + ':' + str(m) + ":00', 1" + str(random.random()) + ")")
		cur.execute("INSERT INTO test (Time, Value) VALUES ('" + 
			date + " " + str(h) + ':' + str(m) + ":00', " +
			str(1 if h > 17 else 0) +
			str(random.random()) + ")")

		m += 5
	h += 1

# cur.execute("INSERT INTO test (Time, Value) VALUES ('" + date + " " + str(h) + ':' + str(m) + ":00', 1" + str(random.random()) + ")")

print("===== Added Rows =====")

cur.execute("SELECT * FROM test")
for row in cur.fetchall():
	print(row)

print("Committing...")
db.commit()
db.close()
