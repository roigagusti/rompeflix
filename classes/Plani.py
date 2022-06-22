from this import s
import requests
import json
import time
import datetime

#user: Agustí
#app: Airtable
class Task():
    def __init__(self, atid, iniciativa, squad, pec_id, owner, tarea, start, end):
        self.atid = atid
        self.iniciativa = iniciativa
        self.squad = squad
        self.pec_id = pec_id
        self.owner = owner
        self.tarea = tarea
        self.start = start
        self.end = end
class Sprint():
    def __init__(self, atid, date, dateRaw, quarter, year, week, sprint):
        self.atid = atid
        self.date = date
        self.dateRaw = dateRaw
        self.quarter = quarter
        self.year = year
        self.week = week
        self.sprint = sprint

def timestampDate(date):
    data = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    return data

class Tasques():
    def __init__(self):
        self.token = 'keyVBM9rXFpJNDEIU'
        self.base_id = 'applVLtXI9jhnWeIB'

    def listTasks(self):
        url = 'https://api.airtable.com/v0/applVLtXI9jhnWeIB/initiatives'
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
                timestampDate(end)
            )
            records.append(tasca)
        
        records.sort(key=lambda x: x.iniciativa)    
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
                record['fields']['Sprint']
            )
            records.append(sprint)
        records.sort(key=lambda x: x.date)
        return records