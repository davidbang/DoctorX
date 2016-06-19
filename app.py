from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db
'''import model as model'''


app=Flask(__name__)
app.config['SECRET_KEY'] = "secret key"

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template ("index.html")



@app.route("/login", methods = ["POST", "GET"])
def login():
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
        
        if (submit == "submit"):
            if (len(l) == 1 and ' ' in l[0]):
                flash("Invalid frees, please separate frees by commas")
                return redirect("/profile/" + str(username))
            l2 = []
            for item in l:
                l2.append(item.strip())
            err = False
            try:
                for item in l2:
                    i = int(item)
                    if (i < 1 or i > 10):
                        err = True
            except:
                flash("Invalid frees, must be numbers")
                return redirect("/profile/" + str(username))
            if err:
                flash("Invalid frees, must be between 1 and 10")
                return redirect("/profile/" + str(username))
            db.change_frees(username, frees)
            return redirect("/profile/" + str(username))
        if (submit1 == "submit"):
            lunch = request.args.get("lname")
            try:
                lunch = int(lunch)
                if (lunch < 4 or lunch > 8):
                    flash("Invalid lunch")
                    return redirect("/profile/" + str(username))
            except:
                flash("Invalid lunch")
                return redirect("/profile/" + str(username))
            db.change_lunch(username, lunch)
            return redirect("/profile/" + str(username))

            
        return render_template ("profile.html", myprofile = myprofile, username2 = username2, data = data)
    else:
        flash ("You are not logged in")
        return redirect ("/")


@app.route("/analysis")
def analysis():
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') == None):
        return redirect("/")
    username = session ['username']
    if (analyze == "analyze"):
        return redirect("/")


    return render_template ("analysis.html", username = username)


@app.route("/results")
def results():
    return render_template ("results.html", username = username)


@app.route("/visuals")
def visuals():
    return render_template ("visuals.html", username = username)


@app.route("/logout")
def logout():
    session.pop('username', None)
    loggedin = False
    flash('You are logged out')
    return redirect("/")


if __name__ == '__main__':
    app.debug = False
    app.run(host = '0.0.0.0', port=8000)