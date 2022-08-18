from this import s
import requests
import json
import time
import datetime

#user: Agustí
#app: Airtable
class Task():
    def __init__(self, atid, iniciativa, squad, pec_id, owner, tarea, start, end,altnum):
        self.atid = atid
        self.iniciativa = iniciativa
        self.squad = squad
        self.pec_id = pec_id
        self.owner = owner
        self.tarea = tarea
        self.start = start
        self.end = end
        self.altnum = altnum
class Hito():
    def __init__(self, atid, iniciativa, start, hito, hitoDate):
        self.atid = atid
        self.iniciativa = iniciativa
        self.start = start
        self.hito = hito
        self.hitoDate = hitoDate
class Habitant():
    def __init__(self, atid, name, short_name):
        self.atid = atid
        self.name = name
        self.short_name = short_name
class Sprint():
    def __init__(self, atid, date, dateRaw, quarter, year, week, sprint,shortname):
        self.atid = atid
        self.date = date
        self.dateRaw = dateRaw
        self.quarter = quarter
        self.year = year
        self.week = week
        self.sprint = sprint
        self.shortname = shortname

def timestampDate(date):
    data = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    return data

class Tasques():
    def __init__(self):
        self.token = 'keyVBM9rXFpJNDEIU'
        self.base_id = 'applVLtXI9jhnWeIB'

    def listTasks(self):
        parameter = "type"
        url = "https://api.airtable.com/v0/applVLtXI9jhnWeIB/initiatives?filterByFormula={type}='tarea'"
        rest = url
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        
        for record in data['records']:            
            if 'pec_id' in record['fields']:
                pec_id = record['fields']['pec_id']
            else:
                pec_id = '-'
            if 'owner' in record['fields']:
                owner = record['fields']['owner']
            else:
                owner = '-'
            if 'start_date' in record['fields']:
                start = record['fields']['start_date'][0]
            else:
                start = '-'
            if 'end_date' in record['fields']:
                end = record['fields']['end_date'][0]
            else:
                end = '-'
            
            
            tasca = Task(
                record['id'],
                record['fields']['iniciativa'],
                record['fields']['squad'],
                pec_id,
                owner,
                record['fields']['tarea'],
                timestampDate(start),
                timestampDate(end),
                record['fields']['#']
            )
            records.append(tasca)
        # records.sort(key=lambda x: x.start) 
        # records.sort(key=lambda x: x.pec_id) 
        # records.sort(key=lambda x: x.squad) 
        # records.sort(key=lambda x: x.iniciativa) 
        records.sort(key=lambda x: x.altnum)   
        return records

    def listHitos(self):
        parameter = "type"
        url = "https://api.airtable.com/v0/applVLtXI9jhnWeIB/initiatives?filterByFormula={type}='hito'"
        rest = url
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        
        for record in data['records']:            
            hito = Hito(
                record['id'],
                record['fields']['iniciativa'],
                timestampDate(record['fields']['start_date'][0]),
                record['fields']['hito'],
                record['fields']['hito_date']
            )
            records.append(hito)  
        return records

    def listSprints(self,year):
        parameter = "Year"
        url = "https://api.airtable.com/v0/applVLtXI9jhnWeIB/sprints?filterByFormula={" + parameter + "}='" + str(year) + "'"
        rest = url
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        
        for record in data['records']:            
            sprint = Sprint(
                record['id'],
                record['fields']['date'],
                timestampDate(record['fields']['date']),
                record['fields']['Quarter'],
                record['fields']['Year'],
                record['fields']['Week'],
                record['fields']['Sprint'],
                record['fields']['Short name']
            )
            records.append(sprint)
        records.sort(key=lambda x: x.date)
        return records

    def listHabitants(self):
        url = "https://api.airtable.com/v0/applVLtXI9jhnWeIB/staff"
        rest = url
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        
        for record in data['records']:            
            habitant = Habitant(
                record['id'],
                record['fields']['name'],
                record['fields']['Short Name']
            )
            records.append(habitant)
        records.sort(key=lambda x: x.name)
        return records