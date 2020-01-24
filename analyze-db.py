from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from matplotlib import dates, pyplot
from datetime import datetime 
import mysql.connector as mariadb
import pandas
import json
import sys

if( len(sys.argv) < 3 ):
    sys.exit("Incorrect number of arguments. Usage: [FILE] [DATE] [Optional: DEGREE]\nClosing...")


# Visualize the Polymonial Regression results
def viz_polynomial(prediction, degree):
    pyplot.plot_date(datetimes, prediction,color='blue', fmt='-')
    pyplot.scatter(datetimes, y, color='red')
    pyplot.title('Power usage (degree {})'.format(degree))
    pyplot.xlabel('Datetime')
    pyplot.ylabel('Power (kW)')
    pyplot.show()
    return

# Create a best fit curve for a given
def fit_polynomial(x, y, degree=4):
    pol_reg = LinearRegression()
    poly_reg = PolynomialFeatures(degree=degree)
    x_poly = poly_reg.fit_transform(x)
    pol_reg.fit(x_poly, y)
    print("Degree: {}, Regression Score: {}".format( degree, pol_reg.score(x_poly,y)) )
    viz_polynomial( pol_reg.predict( poly_reg.fit_transform(x) ), degree )



# Importing the data

db = json.loads( open( sys.argv[1], "r" ).read() )
data = []
i = 0
for row in db['data']:
    if str(sys.argv[2]) in row['Time']:
        timestamp = dates.date2num( datetime.strptime( row['Time'], "%Y-%m-%d %H:%M:%S" ))
        data.append({ "id": i,
                 "Wattage": row['Wattage'],
                    "Time": timestamp })
        i += 1

pandas.plotting.register_matplotlib_converters() # required to use matplotlib.dates 
data = pandas.DataFrame(data)
x         = data.iloc[:, 0:1].values
y         = data.iloc[:, 1].values
datetimes = data.iloc[:, 2].values

# print(data)
# print(x)
# print(y)
# print(datetimes)


# Fitting Polynomial Regression

if( len(sys.argv) == 4 ):
    fit_polynomial(x, y, int(sys.argv[3]))
else:
    fit_polynomial(x, y)

# for i in range(9):
#     fit_polynomial(x, y, i)
