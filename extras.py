import datetime

#display dictionary items as a string
def list(d):
    x = " "
    for k, v in d.items():
        x = x + str(k) + ": " + str(v) + "\n"
    return x

# retrieve the key in a dictionary given its value
def getKey(dct,value):

    return [key for key in dct if (dct[key] == value)]
