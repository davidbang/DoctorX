from havenondemand.hodclient import *
import csv
import random
import os
import errno


client = HODClient('6742a14b-339a-4691-8b09-3e5881e9c641')
serviceName = 'service1'


def connect():
	## Train predictor
	serviceName = 'alzheimerService'
	predictionField = 'alzheimers'
	filePathTrainPredictor = './datasets/train_predictor.csv' # uncomment if using .csv
	# filePathTrainPredictor = './data_sets/train_predictor.json' # uncomment if using .json
	jobID = ''
	dataTrainPredictor = {'file': filePathTrainPredictor, 'prediction_field': predictionField, 'service_name': serviceName}

	r_async = client.post_request(dataTrainPredictor, HODApps.TRAIN_PREDICTOR, async=True)
	jobID = r_async['jobID']
	print jobID

	## Check status of train prediction
	response = client.get_job_status(jobID)
	print response
	return response

def predict(serviceName, st, ss):
	try:
	    os.remove('datasets/predict.csv')
	except OSError as e: # this would be "except OSError, e:" before Python 2.6
	    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
	        pass

	with open('datasets/predict.csv', 'wb') as csvfile:
	   	writer = csv.writer(csvfile)
		fields = ['travel', 'spending', 'alzheimers']

		writer.writerow(fields)
		writer.writerow(['INTEGER','INTEGER','RICH_TEXT'])
		writer.writerow([st, ss,""])

		csvfile.close()

	## Predict
	filePathPredict = './datasets/predict.csv' # uncomment if using .csv
	# filePathPredict = './data_sets/predict.json' # uncomment if using .json
	format = 'csv' # uncomment if wanted response is .csv
	# format = 'json' # uncomment if wanted response is .json
	dataPredict = {'file': filePathPredict, 'service_name': serviceName, 'format': format}

	r_predict = client.post_request(dataPredict, HODApps.PREDICT, async=False)

	print r_predict
	return r_predict

def recommend():
	## Recommend
	filePathRecommend = './datasets/recommend.json'
	requiredLabel = 'blue'
	recommendationsAmount = 3
	dataRecommend = {'file': filePathRecommend, 'service_name': serviceName, 'required_label': requiredLabel}

	r_recommend = client.post_request(dataRecommend, HODApps.RECOMMEND, async=False)
	print r_recommend
