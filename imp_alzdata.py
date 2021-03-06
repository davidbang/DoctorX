import imp
import random
import os
import errno
from scipy import linspace
from scipy import pi,sqrt,exp
from scipy.special import erf

# -*- coding: utf-8 -*-

ax = -122.4067
ay = -75.451355


bx = -122.407
by =  37.782


AGOL = imp.load_source('agol', '/Users/davidbang/DoctorX/agol.py')
module = imp.load_source('network', '/Users/davidbang/DoctorX/network.py')
x = module.networkService("Davidbang12", "Davidbang123")

try:
    os.remove('static/alzheimerstraveldata.json')
    os.remove('static/badtrips.json')
except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
        pass

file = open('static/alzheimerstraveldata.json','w')
a = 8

file2 = open('static/badtrips.json','w')
file2.write("[")

for i in range(0, 1000):
	if (i == 0):
		file.write("[")
	if i > 200:
		a = 7
	if i > 200:
		a = 6
	if i > 400:
		a = 5
	if i > 600:
		a = 4
	if i > 800:
		a = 3

	z = x.routeNetwork()
	y = z[0]
	ay = z[1]

	getTravelTime = y[u'routes'][u'features'][0][u'attributes'][u'Total_TravelTime']
	getTripLength = y[u'routes'][u'features'][0][u'attributes'][u'Total_Miles']
	tmp = getTravelTime
	getFuzziedTravelTime = getTravelTime
	if i % 4 == 0 or i % 4 == 1 or i % 4 == 2 or i < 410:
		getFuzziedTravelTime = abs(random.gauss(tmp, tmp/a))
		if a < 5:
			getFuzziedTravelTime = abs( random.gauss(tmp, tmp/5))
	if i % 4 == 3 and i > 400:
		r = random.uniform(0.5, 1.5)
		getFuzziedTravelTime = abs(r * tmp + random.gauss(tmp, tmp/a))
	if i % 3 == 2 and i > 600:
		r = random.uniform(0.8, 1.8)
		getFuzziedTravelTime = abs(r * tmp + random.gauss(tmp, tmp/a))
	if i % 2 == 1 and i > 800:
		r = random.uniform(1.2, 2.0)
		getFuzziedTravelTime = abs(r * tmp + random.gauss(tmp, tmp/a))
	
	ratio = getFuzziedTravelTime/getTravelTime
	if ratio > 2.0:
		file2.write("[" + str(ax) + ", " + str (ay) + ", "  + str(bx) + ", " + str (by) + "]")


	if ratio < 1:
		ratio = ratio + 0.2 * (1-ratio) 
	getTripLength = ratio * getTripLength 
	file.write("[" + str(getTripLength) + ", " + str(ratio) + "]")
	if (i == 999):
		file.write("]")
	else:
		file.write(",\n")
		if ratio > 2.0:
			file2.write(",\n")
	print str(i)


file2.write("]")


file.close()
file2.close()




