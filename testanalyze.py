from analyzeDB import getDataset, fitRegression, plotRegression

dataset = getDataset(file="db.json", date="2020-01-24")

reg = fitRegression(dataset[0], dataset[1])

plotRegression(dataset[2], reg[0], dataset[1])