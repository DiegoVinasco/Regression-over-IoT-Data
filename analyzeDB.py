from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from matplotlib import dates, pyplot
from datetime import datetime
import pandas
import json
import sys


def getDataset(file, date):

    # Importing the data
    db = json.loads( open( file, "r" ).read() )
    data = []
    i = 0
    for row in db['data']:
        if str(date) in row['Time']:
            timestamp = dates.date2num( datetime.strptime( row['Time'], "%Y-%m-%d %H:%M:%S" ))
            data.append({ "id": i,
                     "Wattage": row['Wattage'],
                        "Time": timestamp })
            i += 1

    pandas.plotting.register_matplotlib_converters() # required to use matplotlib.dates 
    dataset = pandas.DataFrame(data)
    x         = dataset.iloc[:, 0:1].values
    y         = dataset.iloc[:, 1].values
    datetimes = dataset.iloc[:, 2].values

    # Fitting Polynomial Regression
    return [x, y, datetimes]


# Create a best fit curve for a given. Returns an array of best fit points and score
def fitRegression(x, y, degree=4):
    pol_reg = LinearRegression()
    poly_reg = PolynomialFeatures(degree=degree)
    x_poly = poly_reg.fit_transform(x)
    pol_reg.fit(x_poly, y)
    return [pol_reg.predict(x_poly), pol_reg.score(x_poly,y)]

# Visualize the Polymonial Regression results
def plotRegression(datetimes, prediction, y, degree=4):
    pyplot.plot_date(datetimes, prediction,color='blue', fmt='-')
    pyplot.scatter(datetimes, y, color='red')
    pyplot.title('Power usage (degree {})'.format(degree))
    pyplot.xlabel('Datetime')
    pyplot.ylabel('Power (kW)')
    pyplot.show()
    return
