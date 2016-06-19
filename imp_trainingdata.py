import imp
import random
import os
import errno

# -*- coding: utf-8 -*-

ax = -122.4067
ay = -75.451355


bx = -122.407
by =  37.782

AGOL = imp.load_source('agol', '/Users/davidbang/DoctorX/agol.py')
module = imp.load_source('network', '/Users/davidbang/DoctorX/network.py')
x = module.networkService("Davidbang12", "Davidbang123")

try:
    os.remove('static/traintraveldata.json')
except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
        pass

file = open('static/traintraveldata.json','w')


for i in range(0, 1000):
	if (i == 0):
		file.write("[")

	z = x.routeNetwork()
	y = z[0]
	ay = z[1]
	getTravelTime = y[u'routes'][u'features'][0][u'attributes'][u'Total_TravelTime']
	getTripLength = y[u'routes'][u'features'][0][u'attributes'][u'Total_Miles']
	if (i % 4 == 0):
		getFuzziedTravelTime = random.gauss(getTravelTime * 0.8, getTravelTime/8)
	if (i % 4 == 1):
		getFuzziedTravelTime = random.gauss(getTravelTime * 1.2, getTravelTime/8)
	if (i % 4 == 2):
		getFuzziedTravelTime = random.gauss(getTravelTime * 0.8, getTravelTime/8)
	if (i % 4 == 3):
		getFuzziedTravelTime = random.gauss(getTravelTime * 1.2, getTravelTime/8)
	ratio = getFuzziedTravelTime/getTravelTime
	if (i % 4 == 0):
		getTripLength = 0.8 * getTripLength
	if (i % 4 == 1):
		getTripLength = 1.2 * getTripLength
	if (i % 4 == 2):
		getTripLength = 0.8 * getTripLength
	if (i % 4 == 3):
		getTripLength = 1.2 * getTripLength


	file.write("[" + str(getTripLength) + ", " + str(ratio) + "]")
	if (i == 999):
		file.write("]")
	else:
		file.write(",\n")

	print str(i)

file.close()




