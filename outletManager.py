from analyzeDB import getDataset, fitRegression, plotRegression
import sys

degree = 4
if(len(sys.argv) == 2):
	degree = int(sys.argv[1])

dataset = getDataset(file="db.json", date="2020-01-24")
reg = fitRegression(dataset[0], dataset[1], degree)
plotRegression(dataset[2], reg[0], dataset[1], degree)