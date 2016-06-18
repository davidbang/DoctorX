from pymongo import Connection

#client = MongoClient()
#db = client.account_manager

conn = Connection()
db = conn['accountinfo']

users = db.users


#-----USERNAMES-----
def user_auth(username, password): #string, string
    return users.find({'username':username, 'password':password}).count() == 1

def user_exists(username): #string
    return users.find({'username':username}).count() > 0

def user_creat(username, password): #string, string
    if (not user_exists(username)):
        new = { 'username' : username,
                'password' : password,
                'age' : 50,
                'phone': 7183620636,
                'credit': 4207123412341234
                }
        users.insert(new)
        print "Registration successful"
    print "Registration failed; Username taken"


    
def get_user_data(username, data): #string, string
    user = users.find_one({'username':username})
    if (user != None):
        if data in user:
            return user[data]
    print "No %s data for user %s."%(data,username)

def get_all_user_data(username): #string
    user = users.find_one({'username':username})
    user.pop("password", None) #privacy is cool
    return user




