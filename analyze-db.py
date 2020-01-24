from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from matplotlib import dates, pyplot
from datetime import datetime 
import mysql.connector as mariadb
import pandas
import json
import sys

if( len(sys.argv) < 2 ):
    sys.exit("Incorrect number of arguments. Usage: [FILE] [Optional: DEGREE]\nClosing...")

# Visualize the Linear Regression results
def viz_linear():
    pyplot.scatter(x, y, color='red')
    pyplot.plot(x, lin_reg.predict(x), color='blue')
    pyplot.title('Wattage use (Linear)')
    pyplot.xlabel('Time (seconds)') # TODO: visualize timestamp
    pyplot.ylabel('Watts')
    pyplot.show()
    return

# Visualize the Polymonial Regression results
def viz_polynomial(prediction, degree):
    pyplot.scatter(x, y, color='red')
    pyplot.plot(x, prediction, color='blue')
    pyplot.title('Wattage use (degree {})'.format(degree))
    pyplot.xlabel('Time (seconds)')
    pyplot.ylabel('Watts')
    pyplot.show()
    return


# Importing the data

db = json.loads( open( sys.argv[1], "r" ).read() )
data = []
i = 0
for row in db['data']:
    timestamp = dates.date2num( datetime.strptime( row['Time'], "%Y-%m-%d %H:%M:%S" ))
    data.append({ "id": i,
             "Wattage": row['Wattage'],
                "Time": timestamp })
    i += 1

data = pandas.DataFrame(data)
x = data.iloc[:, 0:1].values # TODO: implement timestamp into regression
y = data.iloc[:, 1].values

# print(x)
# print(y)


# Fitting Linear Regression (no longer used; switched to polynomial)
# lin_reg = LinearRegression()
# lin_reg.fit(x, y)


# print("Linear Regression Score: {}".format(lin_reg.score(x,y)))
# viz_linear()



# Fitting Polynomial Regression

deg = 4
if( len(sys.argv) == 3 ):
    deg = int(sys.argv[2])

pol_reg = LinearRegression()
poly_reg = PolynomialFeatures(degree=deg)
x_poly = poly_reg.fit_transform(x)
pol_reg.fit(x_poly, y)
viz_polynomial( pol_reg.predict( poly_reg.fit_transform(x) ), deg )



print("Polynomial Regression Score:")
print("Degree: {}, Score: {}".format( deg, pol_reg.score(x_poly,y)) )
