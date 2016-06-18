import numpy as np
import skfuzzy
import datetime
import json
import math
import SimpleHTTPServer
from googlemaps import convert
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import googlemaps
from datetime import datetime
from flask import Flask, request
import cgi
import matplotlib
import matplotlib.pyplot as plt


THRESHHOLD_CONSTANT=0.2
global testing
global u

with open("static/data.json", "r") as datafile:
    testing= json.load(datafile)

PORT = 5000



"""JSON loads whatever  Parth sent"""

"""Train cluster on past 500 data points"""

print "Building model..."


def formatInput(inputList):
    inputFormatted = [None]*len(inputList)
    for i in xrange(len(inputList)):
        inputFormatted[i]=np.array(inputList[i])
    print np.array(inputFormatted)
    return np.array(inputFormatted).T

def getCenter(pieceStack):
    center, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(
        pieceStack, 2, 2, error=0.004, maxiter=5000)
    return center

def getU(pieceStack):
    center, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(
        pieceStack, 2, 2, error=0.004, maxiter=5000)
    return u

def predict(newPurchaseList, center):
    u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans_predict(newPurchaseList, center, 2, error=0.003333, maxiter=2500)
    return np.argmax(u, axis=0)

def lastNs(formatting, n):
    print (-n+1)
    return formatInput(formatting[-(n+1)::])

#computes whether  dementia is increasing or decreasing beyond a certain threshold
def deltaRate(someList):
    return [scoreDeltaN(someList, int(math.pow((5),(i+1)))) for i  in range(0,5)]

def getNumAlzheimers(someList):
    getting=formatInput(someList)
    u=getU(np.array(getting))
    clusters= np.argmax(u, axis=0)
    print

def scoreDeltaN(someList, n):
    lastN = lastNs(someList, n)
    firstN = formatInput(someList[::n])
    centers=getCenter(np.array(firstN))
    centers=getCenter(np.array(lastN)) 
    predictionsLast=predict(lastN, centers)
    firstClassifications= predict(firstN, centers)
    priorRate = np.sum(firstClassifications)/float(len(someList))
    posteriorRate = np.sum(predictionsLast)/float(n)
    return (posteriorRate-priorRate)


def checkDementia(inputList):
    inputFormatted= formatInput(inputList)
    center=getCenter(inputFormatted)
    print "Delta  Rate: " + str(sum(deltaRate(inputList))/5.0)
    print getNumAlzheimers(inputList)
"""
    last10=lastN(inputList, 10) 
    last25= lastN(inputList, 25)
    last50= lastN(inputList, 50)
    print predict(last10, center)"""
    #sort numpy array
    #grab 5, 25, 50 last purchases delta
    #grab 
checkDementia(testing)

gmaps = googlemaps.Client(key='AIzaSyD2NVFv0HSTEnr0RSGkBAwLEi75Odh3rbU')


# Request directions via public transit

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_data():
    form = cgi.FieldStorage()
    print "The user entered %s" % form.getvalue("uservalue")
    print "Hello World - you sent me " + str(request.values)
    return "Hello World - you sent me " + str(request.values)



def determineExpectedTime(start, end):
    now = datetime.now()
    directions_result = gmaps.directions(start,
                                     end,
                                     mode="driving",
                                     departure_time=now)
    extracted=str(directions_result[0]["legs"][0]["duration_in_traffic"]["text"])
   
    expectedList = [int(s) for s in extracted.split() if s.isdigit()]
    expectedMS = expectedList[0]*3600*1000+expectedList[1]*60*1000
    return expectedMS


def getDifferentOfExpected(someAndroidLocObject):
    startLat=someAndroidLocObject[0]
    startLong=someAndroidLocObject[1]
    endLat=someAndroidLocObject[2]
    endLong=someAndroidLocObject[3]
    totalTime= someAndroidLocObject[4]

    if ((totalTime-(determineExpectedTime((startLat,startLong), (endLat, endLong))))/float(totalTime))>0.10:
       return 1
    else:
       return 0

def handleDifferentTimes(someAndroidLocObject):
   with open("geolocData.json", "r") as infile:
        d=json.load(infile)
   d=d.append(getDifferentOfExpected(someAndroidLocalObject))
   with open("geolocData.json", "w") as outfile:
        outfile.write(json.dumps(d))
   return sum(d)/float(len(d))

print determineExpectedTime((38.927, -77.234),(36.284, -78.321))

testing2 = np.array(formatInput(testing))

center,u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(testing2, 2, 2, error=0.004, maxiter=5000)


fig2, ax2 = plt.subplots()
ax2.set_title('Trained model')
for j in range(2):
    ax2.plot(testing2[0, u.argmax(axis=0) == j],
             testing2[1, u.argmax(axis=0) == j], 'o',
             label='series ' + str(j))
ax2.legend()

plt.savefig('foo.png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"))