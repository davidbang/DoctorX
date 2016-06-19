import numpy as np
import skfuzzy
import datetime
import json
import math
from datetime import datetime
import cgi
import matplotlib
import matplotlib.pyplot as plt
import random
import haven as hp
from havenondemand.hodclient import *



THRESHHOLD_CONSTANT=0.2
global testing
global u
global traintravel
global trainspending2
with open("static/data.json", "r") as datafile:
    testing= json.load(datafile)


"""Train cluster on past 1000 data points"""

print "Building model..."

#modelid = hp.connect()

#print "Connecting to HP. Training Model"

prediction = hp.predict('alzheimerService', 60, 60)

print prediction[u'file']

if "True" in prediction[u'file']:
    print "TRUE"

def formatInput(inputList):
    inputFormatted = [None]*len(inputList)
    for i in xrange(len(inputList)):
        inputFormatted[i]=np.array(inputList[i])
    print np.array(inputFormatted)
    return np.array(inputFormatted).T


def lastN(formatting, n):
    print (-n+1)
    return formatInput(formatting[-(n+1)::])

def runModel():

    with open("static/traintraveldata.json", "r") as datafile:
        traintravel= json.load(datafile)

    traintravel2 = formatInput(traintravel)
    center,u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(traintravel2, 4, 4, error=0.004, maxiter=5000)


    index = 0
    max = 0
    for i in range (0,4):
        if center[i][1] > max:
            index = i
            max = center[i][1]

    index2 = 0
    max = 0
    for i in range (0,4):
        if center[i][1] > max and (not (index == i)):
            index2 = i
            max = center[i][1]

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    print lenbad
    print lenbad2
    percentagebad = float((lenbad + lenbad2) / 1000.0)


    fig2, ax2 = plt.subplots()
    ax2.set_title('Trained Travel Model')
    plt.ylabel('Actual Travel Time to Estimated Travel Time Ratio')
    plt.xlabel('Actual Travel Distance')
    for j in range(4):
        if j == index or j == index2:
            ax2.plot(traintravel2[0, u.argmax(axis=0) == j],
                 traintravel2[1, u.argmax(axis=0) == j], 'o',
                 label='Alzheimer Cluster ')
        else:
            ax2.plot(traintravel2[0, u.argmax(axis=0) == j],
                 traintravel2[1, u.argmax(axis=0) == j], 'o',
                 label='Normal Cluster ')


    ax2.legend()

    plt.savefig('static/trainedtravel.png')

    plt.clf()


    a = traintravel2[0, u.argmax(axis=0) == 1]


    with open("static/alzheimerstraveldata.json", "r") as datafile:
        traintravel= json.load(datafile)

    counter = 0

    '''Start derivative block'''

    traintravel2 = lastN(traintravel, 800)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 800.0)):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 800.0


    traintravel2 = lastN(traintravel, 600)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 600.0)):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 600.0

    traintravel2 = lastN(traintravel, 500)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 500.0)):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 500.0


    traintravel2 = lastN(traintravel, 400)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 400.0)):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 400.0


    traintravel2 = lastN(traintravel, 300)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 300.0)):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 300.0



    traintravel2 = lastN(traintravel, 200)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)


    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad <((lenbad + lenbad2) / 200.0)):
        counter += 2
    percentagebad = (lenbad + lenbad2) / 200.0


    traintravel2 = lastN(traintravel, 100)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 100.0)):
        counter += 2
    percentagebad = (lenbad + lenbad2) / 100.0

    traintravel2 = lastN(traintravel, 50)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 50.0)):
        counter += 3
    percentagebad = (lenbad + lenbad2) / 50.0

    traintravel2 = lastN(traintravel, 25)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]
    b = traintravel2[1, u.argmax(axis=0) == index2]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < ((lenbad + lenbad2) / 25.0)):
        counter += 3
    percentagebad = (lenbad + lenbad2) / 25.0

    '''End derivative block'''

    scoretravel = random.gauss(counter/15.0, 0.05)

    print "SCORETRAVEL:" + str(scoretravel)

    traintravel2 = formatInput(traintravel)


    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)


    cluster_membership = np.argmax(u, axis=0)  # Hardening for visualization
    traintravel2 = formatInput(traintravel2)
    fig3, ax3 = plt.subplots()
    ax3.set_title("Alzheimer's Travel Model")
    plt.ylabel('Actual Travel Time to Estimated Travel Time Ratio')
    plt.xlabel('Actual Travel Distance')
    for j in range(4):
        if j == index or j == index2:
            ax3.plot(traintravel2[cluster_membership == j, 0],
                     traintravel2[cluster_membership == j, 1], 'o',
                     label='Alzheimer Cluster ')
        else:
            ax3.plot(traintravel2[cluster_membership == j, 0],
                    traintravel2[cluster_membership == j, 1], 'o',
                    label='Normal Cluster ')
    ax3.legend()

    plt.savefig('static/alzheimerstravel.png')
    plt.clf()



    with open("static/trainspendingdata.json", "r") as datafile:
        trainspending2 = json.load(datafile)


    trainspending3 = formatInput(trainspending2)
    center,u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(trainspending3, 3, 3, error=0.004, maxiter=5000)


    index = 0
    max = 0
    for i in range (0,3):
        if center[i][0] > max:
            index = i
            max = center[i][0]


    fig2, ax2 = plt.subplots()
    ax2.set_title('Trained Spending Model')
    plt.ylabel('Money Spent')
    plt.xlabel('Buying Index')
    for j in range(3):
        if j == index:
            ax2.plot(trainspending3[0, u.argmax(axis=0) == j],
                 trainspending3[1, u.argmax(axis=0) == j], 'o',
                 label='Alzheimer Cluster ')
        else:
            ax2.plot(trainspending3[0, u.argmax(axis=0) == j],
                 trainspending3[1, u.argmax(axis=0) == j], 'o',
                 label='Normal Cluster ')
    ax2.legend()

    plt.savefig('static/trainedspending.png')
    plt.clf()



    with open("static/alzheimersspendingdata.json", "r") as datafile:
        trainspending2 = json.load(datafile)

    counter = 0

    '''Start derivative block'''

    traintravel2 = lastN(trainspending2, 450)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 450.0):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 450.0

    traintravel2 = lastN(trainspending2, 400)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 400.0):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 400.0

    traintravel2 = lastN(trainspending2, 300)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 300.0):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 300.0


    traintravel2 = lastN(trainspending2, 250)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 250.0):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 250.0


    traintravel2 = lastN(trainspending2, 200)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 200.0):
        counter += 1
    percentagebad = (lenbad + lenbad2) / 200.0



    traintravel2 = lastN(trainspending2, 150)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)


    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad <(lenbad + lenbad2) / 150.0):
        counter += 2
    percentagebad = (lenbad + lenbad2) / 150.0


    traintravel2 = lastN(trainspending2, 100)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 100.0):
        counter += 2
    percentagebad = (lenbad + lenbad2) / 100.0

    traintravel2 = lastN(trainspending2, 50)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 50.0):
        counter += 3
    percentagebad = (lenbad + lenbad2) / 50.0

    traintravel2 = lastN(trainspending2, 20)

    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        traintravel2, center, 8 , error=0.004, maxiter=5000)

    a = traintravel2[1, u.argmax(axis=0) == index]

    lenbad = len(a.tolist())
    lenbad2 = len(b.tolist())
    if (percentagebad < (lenbad + lenbad2) / 20.0):
        counter += 3
    percentagebad = (lenbad + lenbad2) / 20.0

    '''End derivative block'''

    scorespending = random.gauss(counter/15.0, 0.05)

    print "SCORESPENDING:" + str(scorespending)


    trainspending3 = formatInput(trainspending2)
    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(
        trainspending3, center, 3 , error=0.004, maxiter=5000)

    fig2, ax2 = plt.subplots()
    ax2.set_title("Alzheimer's Spending Model")
    plt.ylabel('Money Spent')
    plt.xlabel('Buying Index')
    for j in range(3):
        if j == index:
            ax2.plot(trainspending3[0, u.argmax(axis=0) == j],
                 trainspending3[1, u.argmax(axis=0) == j], 'o',
                 label='Alzheimer Cluster ')
        else:
            ax2.plot(trainspending3[0, u.argmax(axis=0) == j],
                 trainspending3[1, u.argmax(axis=0) == j], 'o',
                 label='Normal Cluster ')
    ax2.legend()

    plt.savefig('static/alzheimerspending.png')
    plt.clf()

    print "SCORE TRAVELING:" + str(scoretravel)

    print "SCORE SPENDING:" + str(scorespending)

    print "Connecting to HP Prediction Model"

    scoretravel = int(scoretravel * 100)
    scorespending = int(scorespending * 100)

    prediction = hp.predict('alzheimerService', scoretravel, scorespending)
    prediction = hp.predict('alzheimerService', 60, 60)

    print prediction[u'file']
    weight = 0
    if "True" in prediction[u'file']:
        weight = 1

    return [scoretravel, scorespending, weight]
