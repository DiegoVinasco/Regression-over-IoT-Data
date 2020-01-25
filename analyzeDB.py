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
    return dataset


# Create a best fit curve for a given. Returns an array of best fit points and score
def fitRegression(x, y, degree=4):
    pol_reg = LinearRegression()
    poly_reg = PolynomialFeatures(degree=degree)
    x_poly = poly_reg.fit_transform(x)
    pol_reg.fit(x_poly, y)
    return [pol_reg.predict(x_poly), pol_reg.score(x_poly,y)]


# Visualize the Polymonial Regression results. 'predictions' takes a list of fit polynomial lines to plot
def plotRegression(predictions, datetimes, y):
    for prediction in predictions:
        pyplot.plot_date(datetimes, prediction[0], fmt='-', label="Degree: {}".format(str(prediction[1])) )
    pyplot.scatter(datetimes, y, color='red')
    pyplot.title('Power usage')
    pyplot.xlabel('Datetime')
    pyplot.ylabel('Power (kW)')
    pyplot.legend()
    pyplot.show()
    return

# Create an OpenHAB rulefile based on our predicted strategy
def createRuleFile(strategy, file="predicted.rules"):
    buff =  'rule "Light ON"\nwhen\n'
    for change in strategy:
        if (change[0]): # If strategy is true write timestamp of change to file
            buff += '  Time cron "{}"\n'.format(change[1])
    buff += 'then\n  Sensor_A_Switch.sendCommand(ON)\nend\n\nrule "Light OFF"\nwhen\n'
    for change in strategy:
        if (not change[0]): # If strategy is false write timestamp of change to file
            buff += '  Time cron "{}"\n'.format(change[1])
    buff += 'then\n  Sensor_A_Switch.sendCommand(OFF)\nend\n'

    # print(buff)
    f = open(file, "w")
    f.write(buff)
    f.close()




# ===== MAIN =====

dataset = getDataset(file="db.json", date="2020-01-24")
x         = dataset.iloc[:, 0:1].values
y         = dataset.iloc[:, 1].values
datetimes = dataset.iloc[:, 2].values

# Find best fit regression
# regressions = []
# print("Regression scores:")
# for degree in range(1, 6):
#     fit = fitRegression(x, y, degree)
#     regressions.append([fit[0], degree])
#     print("Degree: {}, R^2: {}".format(degree, fit[1]) )
# plotRegression(regressions, datetimes, y)

### Degree 4 or 5 appear to be the best polynomial fits for a single day of data!


# Determine a strategy for when to power the outlet
pol_reg = LinearRegression()
poly_reg = PolynomialFeatures(degree=5)
x_poly = poly_reg.fit_transform(x)
pol_reg.fit(x_poly, y)

predictions = pol_reg.predict(x_poly)
strategy = []
outlet_on = predictions[0] > 0.5
i = 0
for prediction in predictions:
    new_state = prediction > 0.5
    if ( outlet_on != new_state ): # if predicted state changed from previous timestamp, log timestamp and change
        outlet_on = new_state
        strategy.append([ outlet_on, dates.num2date(datetimes[i]).strftime('%S %M %H * * * ?') ])
    i += 1

print(strategy)
createRuleFile(strategy=strategy)