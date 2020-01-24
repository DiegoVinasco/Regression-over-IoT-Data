# Regression-over-IoT-Data
 Pull IoT sensor data from mariadb and analyse it with sklearn
 
## Overview
 This project uses python scripts to interface with a remote mariadb server. The original sensor data is being pulled from a TP-Link HS110 smart outlet interfacing with a local OpenHAB server running on a raspberry Pi. This local server logs incoming sensor data to an OpenHAB Cloud server running on an EC2 AWS.
 Here is where our python scripts will analyze the logged data from mariadb.

## Usage
import-db.py is used to import data from a specified mariadb server and output a json file with it's contents.

analyze-db.py is used to perform polynomial regression on the dataset using sklearn and display it through matplotlib