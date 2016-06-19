import json
import ast
import numpy as np
import random
import os
import errno


global testing
global testing2

with open("static/data.json", "r") as datafile:
    testing= json.load(datafile)

data = np.array(testing)
numpydata = data[:, 5]
datalist = np.array(testing).tolist()
numpydata2 = numpydata.tolist()
newlist = []
newlist2 = []

numpyamount = data[:, 3]
amountlist = numpyamount.tolist()

try:
    os.remove('static/trainspendingdata.json')
except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
        pass

file = open('static/trainspendingdata.json','w')

file.write("[")


for x in numpydata2:
	a = 300 - numpydata2.count(x)
	noise = abs(random.gauss(a, a /2))
	newlist.append(noise)

for i in range(0,500):
	z = amountlist[i]
	noise = abs(random.gauss(z, newlist[i] /3))
	newlist2.append(noise)

for y in range(0, 500):
	file.write("[" + str(newlist[y]) + ", " + str(newlist2[y]) + "]")
	if not (y == 499):
		file.write(",\n")


file.write("]")
file.close()

with open("static/trainspendingdata.json", "r") as datafile:
    testing2= json.load(datafile)

data = np.array(testing2)
normalizedata = data.tolist()
tmplist = []


try:
    os.remove('static/alzheimersspendingdata.json')
except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
        pass

file = open('static/alzheimersspendingdata.json','w')
file.write("[")


for y in range(0, 500):
	xy = normalizedata[y]
	index = xy[0]
	cost = xy[1]

	value = random.gauss(10.1, 1.0)  * 500
	compare = random.gauss(10.2, 0.8) * 500
	if y >100:
		value = random.gauss(10.1, 1.0)  * 500
		compare = random.gauss(10.0, 0.8) * 500
	if y > 200:
		value = random.gauss(10.35, 1.0)  * 500
		compare = random.gauss(10.0, 0.8) * 500
	if y > 300:
		value = random.gauss(10.55, 1.0)  * 500
		compare = random.gauss(10.0, 0.8) * 500
	if y > 400:
		value = random.gauss(10.75, 1.0)  * 500
		compare = random.gauss(10.0, 0.8) * 500
	if value > compare:
		index = index * abs(random.gauss(2.8, 1.2))
		cost = cost * abs(random.gauss(2.8, 1.2))

	noise = abs(random.gauss(1.00100, 0.0100))
  	index = noise * index
  	cost = cost * noise

	file.write("[" + str(index) + ", " + str(cost) + "]")
	if not (y == 499):
		file.write(",\n")


file.write("]")
file.close()
