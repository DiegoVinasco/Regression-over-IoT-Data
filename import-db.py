from datetime import datetime
import mysql.connector as mariadb
import sys

if(len(sys.argv) != 6):
	sys.exit("Incorrect number of arguments. Usage: [FILE] [HOST] [USER] [PASSWORD] [DATABASE]\nClosing...")	

# Connect to local mariadb server
db = mariadb.connect(
    host=sys.argv[2],
    user=sys.argv[3],
    passwd=sys.argv[4],
    database=sys.argv[5]
)

cur = db.cursor()
cur.execute("SELECT * FROM Item2")


# Format data into json eg:
# {"data" : [
# 	{
# 		"Time": timestamp,
# 		"Wattage": value
# 	}
# ]}

data = '{"data":['
for row in cur.fetchall():
	data += '{"Time":"' + row[0].strftime('%Y-%m-%d %H:%M:%S') + '",'
	data += '"Wattage":' + str(row[1]) + "},"
data = data[:-1] + "]}"

cur.close()

# Write to specified file 
# print(data)
f = open(sys.argv[1], "w")
f.write(data)
f.close()