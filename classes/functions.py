import time
import datetime

def dateToYear(numero):
    string = str(numero)
    date = datetime.datetime.strptime(string,"%Y-%m-%d")
    year = date.strftime("%m.%Y")
    return year