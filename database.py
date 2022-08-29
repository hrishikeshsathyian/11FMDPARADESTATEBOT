import pymongo
import certifi
import pprint
from pymongo import MongoClient
from datetime import datetime
import pytz

ca = certifi.where()
cluster = MongoClient("mongodb+srv://hrishikeshsathyian:T0212343B@cluster0.6lfkxzp.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = cluster["TestDatabase"]
NR = db["nominal_roll"]

#gets total strength of the platoon by reading the databse
def getStrength():
    value = NR.count_documents({})
    return str(value)
#adds a user to the collection
def addUser(tele_id,username,platoon):
    NR.insert_one({"_id": tele_id,"username":username,"platoon":platoon,"perma":"DISABLED"})
# removes a user from the collection
def removeUser(username):
    NR.delete_one({"username":username})

# displays all the users and states ID USER NAME and PLATOON
def displayNR():
    x = " "
    n = 1
    cursor = NR.find({})
    for document in cursor:
        x = x + str(n) + ") " + document["username"] + " | " + document["platoon"] + "\n"
        n = n + 1
    return x



def restartPS():
    cursor = NR.find({})
    for document in cursor:
        if document["perma"] == "DISABLED":
            NR.update_one({"username":document["username"]},{"$set" : {"value": "NULL"}})
        else:
            NR.update_one({"username":document["username"]},{"$set" : {"value": document["perma"]}})


def getUser(id):
    cursor = NR.find({})
    for document in cursor:
        if id == document["_id"] or id == document["username"]:
            return document["username"] + "-" + document["platoon"]
            break
        else:
            continue
def getIn(value):
    x=0
    cursor = NR.find({})
    for document in cursor:
        if document["value"].split()[0].upper() == value:
            x = x + 1
        else:
            continue
    return x

def UserExists(value):
    x = 0
    cursor = NR.find({})
    for document in cursor:
        if document["username"] == value or document["_id"] == value:
            x = x + 1
        else:
            continue
    if x == 1:
        return True
    else:
        return False

def changeValue(value,identification):
    try:
        x = NR.find({"username": identification})[0]
        username = x["username"]
        NR.update_one({"username":username},{"$set":{"value":value}})
    except IndexError:
        x = NR.find({"_id": identification})[0]
        username = x["username"]
        NR.update_one({"username":username},{"$set":{"value":value}})


def getState(status):
    x = ""
    list_42FMP = []
    list_FMW1 = []
    list_FMW2 = []
    list_HQ = []
    number = 1
    for dataset in NR.find({}):
        y = dataset["value"].split()
        if y[0] == status:
            user_platoon = NR.find({"username": dataset["username"]})[0]["platoon"]
            if user_platoon == "42FMP":
                list_42FMP.append(dataset["username"] + "-" + dataset["platoon"] + " " + " ".join(y[1:]).upper())
            elif user_platoon == "FMW1":
                list_FMW1.append(dataset["username"] + "-" + dataset["platoon"]+ " " + " ".join(y[1:]).upper())
            elif user_platoon == "FMW2":
                list_FMW2.append(dataset["username"] + "-" + dataset["platoon"]+ " " + " ".join(y[1:]).upper())
            elif user_platoon == "HQ":
                list_HQ.append(dataset["username"] + "-" + dataset["platoon"]+ " " + " ".join(y[1:]).upper())

    final_list = list_42FMP + list_FMW1 + list_FMW2 + list_HQ
    for i in final_list:
        x = x + "\n" + "{})".format(number) + " " + i
        number += 1
    return x

def returnStrength(value):
    count = (NR.count_documents( { 'value' : { '$regex' : value}} ))
    if value == "IN":
        return "STAY-OUT" + " : " + str(count)
    else:
        return value + " : " + str(count)
def NightStrength():
    text = "Total Strength : {}".format(getStrength()) + "\n" + "Stay In: {}".format(getIn("STAY-IN")) + "\n" + "Stay Out: {}".format(getIn("IN")) + "\n" + "OFF: {}".format(getIn("OFF")) + "\n" + "LEAVE: {}".format(getIn("LEAVE")) + "\n" + "DUTY: {}".format(getIn("DUTY")) + "\n" + "MA: {}".format(getIn("MA")) + "\n" + "MC: {}".format(getIn("MC")) + "\n" + "RSO: {}".format(getIn("RSO")) + "\n" + "RSI: {}".format(getIn("RSI")) + "\n" + "OTHERS: {}".format(getIn("OTHERS")) + "\n" + "AO: {}".format(getIn("AO")) + "\n" + "OS: {}".format(getIn("OS")) + "\n" + "CSE: {}".format(getIn("CSE")) + "\n"
    return text





def NRLIST():
    list = []
    for x in NR.find({},{ "_id": 0, "username": 1,}):
      list.append(x["username"])
    print(list)
    return list


def activateperma(user,data):
    cursor = NR.find({})
    for document in cursor:
        if document["username"] == user:
            NR.update_one({"username":user},{"$set" : {"perma": " ".join(data)}})
            NR.update_one({"username":user},{"$set" : {"value": document["perma"]}})
        else:
            continue

def disableperma(user):
    cursor = NR.find({})
    for document in cursor:
        if document["username"] == user:
            NR.update_one({"username":user},{"$set" : {"perma":"DISABLED"}})
        else:
            continue


tz_singapore = pytz.timezone('Asia/Singapore')
todays_date = tz_singapore.localize(datetime.now()).strftime('%d-%b-%Y')
print(todays_date)

# g = ["LTA", "HRISHI", "AO", "XWB"]
# user_to_be_changed = [name for name in NRLIST() if (name in " ".join(g).upper())][0]
# user_to_be_changed_modified = getUser(user_to_be_changed)
# extra_data = [x for x in [k.upper() for k in g] if x not in user_to_be_changed.split()]
# # activateperma(user_to_be_changed,extra_data)
