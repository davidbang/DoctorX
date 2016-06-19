import csv
import random
import os
import errno

global writer

try:
    os.remove('datasets/train_predictor.csv')
except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
        pass



with open('datasets/train_predictor.csv', 'wb') as csvfile:
   	writer = csv.writer(csvfile)
	fields = ['travel', 'spending', 'alzheimers']

	writer.writerow(fields)
	writer.writerow(['INTEGER','INTEGER','RICH_TEXT'])
	for i in range(0,200):
		if (i % 2 == 0):
			x = int(random.gauss(0.4, 0.1) * 100)
			y = int(random.gauss(0.4, 0.1) * 100 )
			z = False
			data = [x,y,z]
			writer.writerow(data)

		if (i % 2 == 1):
			x = int(random.gauss(0.6, 0.1) * 100)
			y = int(random.gauss(0.6, 0.1) * 100)
			z = True
			data = [x,y,z]
			writer.writerow(data)

	csvfile.close()


