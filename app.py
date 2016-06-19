from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db
import model as model
import twilio.twiml
from twilio.rest import TwilioRestClient
import random

account_sid = "AC26f1116a29d460e5dbfb4334d349f064"
auth_token = "69ac4ba053aa357aa4c998681ef97e12"
client = TwilioRestClient(account_sid, auth_token)

global Alz  
Alz = [60.0,60.0, 1]
global mapindexing
mapindexing = 0

app=Flask(__name__)
app.config['SECRET_KEY'] = "secret key"

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/", methods = ["POST", "GET"])
def index():    
    return render_template ("index.html")



@app.route("/login", methods = ["POST", "GET"])
def login():
    session.pop('username', None)
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect("/profile/" + str (session.get('username')))
    session ['username'] = None
    submit = request.args.get("submit")
    if (submit == "Submit"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_auth(username, password);
        if (does_account_exist == True):
            user = db.get_all_user_data (username)
            session ['username'] = username
            return redirect("/profile/" + str (username))
        flash ("Invalid Username or Password")
        return redirect ("/login")
    return render_template ("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    session.pop('username', None)
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect ("/")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_exists(username)
        if (does_account_exist):
            print("Failed 1")
            return redirect("/register")
        elif (len(username)<1):
            print("Failed 2")
            return redirect("/register")
        else:
            db.user_creat (username, password)
            flash("Successfully registered")
            return redirect ("/")
    return render_template ("register.html") #have a button that redirects to /


@app.route("/profile2", methods = ["POST", "GET"])
def profile2():
    submit = request.args.get("submit")
    if (submit == "Submit"):
        does_account_exist = db.user_auth(username, password);
        if (does_account_exist == True):
            user = db.get_all_user_data (username)
            session ['username'] = username
            return redirect("/profile/" + str(username))
    update = request.args.get("Update")
    if (update == "Update"):
        return redirect("/profileupdate/" + str(username))
    diagnosis = request.args.get("Diagnosis")
    if (diagnosis == "Diagnosis"):
        return redirect("/analysis")

    return render_template ("profile.html")

@app.route("/profile/<username>", methods = ["POST", "GET"])
def profile(username):
    if (username == None):
        flash("invalid page")
        return redirect("/")
    if ('username' in session):
        username2 = session ['username']
        data = db.get_all_user_data (username)
        if (username == username2):
            myprofile = True
        else:
            myprofile = False
    submit = request.args.get("submit")
    if (submit == "Submit"):
        does_account_exist = db.user_auth(username, password);
        if (does_account_exist == True):
            user = db.get_all_user_data (username)
            session ['username'] = username
            return redirect("/profile/" + str(username))
    update = request.args.get("Update")
    if (update == "Update"):
        return redirect("/profileupdate/" + str(username))
    diagnosis = request.args.get("Diagnosis")
    if (diagnosis == "Diagnosis"):
        return redirect("/analysis")

    return render_template ("profile.html")

@app.route("/profileupdate/<username>", methods = ["POST", "GET"])
def profileupdate(username):
    if (username == None):
        flash("invalid page")
        return redirect("/")
    if ('username' in session):
        username2 = session ['username']
        data = db.get_all_user_data (username)
        if (username == username2):
            myprofile = True
        else:
            myprofile = False
    submit = request.args.get("Update")
    if (submit == "Update"):
        '''username = request.args.get("username")
        password = request.args.get("password")'''
        return redirect("/profile/"+ str(username))
    return render_template ("profileupdate.html")


@app.route("/analysis")
def analysis():
    print "Running Model...."
    Alz = model.runModel()
    print "Running Model"
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') == None):
        username = session ['username']
    results = request.args.get("Results")
    if (results == "Results"):
        return redirect("/results")
    return render_template("analysis.html")


@app.route("/results")
def results():
    xcoeff = 1 - Alz[0]
    ycoeff = 1- Alz[1]
    weight2 = Alz[2]
    weight = 0.43 * xcoeff + 0.57 * ycoeff
    age = 59 
    probabilty = 41.0
    if weight2 == 1:
        probabilty = random.gauss(80, 0.10 * weight)
    if weight2 == 0:
        probabilty = random.gauss((age - 10), 2 * weight)
    if probabilty > 100.0:
        probabilty = 93.23
    fl = probabilty - 5.3
    fm = probabilty + 3.5
    if probabilty > 40.0:
        message = "Doctor!!!! Hermione has a high chance of having Alzheimer's!"
    else:
        message = "Doctor!!!! Hermione has a chance of having Alzheimer's!"

    SMS = request.args.get("sendSMS")
    if (SMS == "sendSMS"):
        message = client.messages.create(to="+17183620636", from_="+16465863825",
            body=message)  
        return redirect("/results")

    return render_template ("results.html", message=message, probabilty = str(probabilty), fl = str(fl), fm = str(fm))

@app.route("/SMS")
def SMS():
    xcoeff = 1 - Alz[0]
    ycoeff = 1- Alz[1]
    weight2 = Alz[2]
    weight = 0.43 * xcoeff + 0.57 * ycoeff
    age = 59 
    probabilty = 41.0
    if weight2 == 1:
        probabilty = random.gauss(age, 7 * weight)
    if weight2 == 0:
        probabilty = random.gauss((age - 10), 7 * weight)
    if probabilty > 40.0:
        message = "Doctor!!!! Hermione has a high chance of having Alzheimer's Disease!"
    elif probabilty > 20.0:
        message = "Doctor!!!! Hermione has a chance of having Alzheimer's Disease!"
    else:
        message = "Doctor!!!! Hermione doesn't seem to have a high chance of having Alzheimer's Disease!"

    SMS = request.args.get("sendSMS")
    
    message = client.messages.create(to="+17183620636", from_="+16465863825",
        body=message)  
    return redirect("/results")

@app.route("/mappy")
def maps():
    return render_template ("esri.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    loggedin = False
    flash('You are logged out')
    return redirect("/")


if __name__ == '__main__':
    app.debug = False
    app.run(host = '0.0.0.0', port=8023)