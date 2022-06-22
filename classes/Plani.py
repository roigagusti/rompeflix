from this import s
import requests
import json

#user: Agustí
#app: Airtable
class Task():
    def __init__(self, atid, iniciativa, squad, pec_id, owner, tarea):
        self.atid = atid
        self.iniciativa = iniciativa
        self.squad = squad
        self.pec_id = pec_id
        self.owner = owner
        self.tarea = tarea

class Tasques():
    def __init__(self):
        self.token = 'keyVBM9rXFpJNDEIU'
        self.base_id = 'applVLtXI9jhnWeIB'

    def list(self):
        url = 'https://api.airtable.com/v0/applVLtXI9jhnWeIB/initiatives'
        rest = url
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        
        for record in data['records']:
            if 'iniciativa' in record['fields']:
                iniciativa = record['fields']['iniciativa']
            else:
                iniciativa = '-'
            if 'squad' in record['fields']:
                squad = record['fields']['squad']
            else:
                squad = '-'
            if 'pec_id' in record['fields']:
                pec_id = record['fields']['pec_id']
            else:
                pec_id = '-'
            if 'owner' in record['fields']:
                owner = record['fields']['owner']
            else:
                owner = '-'
            if 'tarea' in record['fields']:
                tarea = record['fields']['tarea']
            else:
                tarea = '-'
            
            
            tasca = Task(
                record['id'],
                iniciativa,
                squad,
                pec_id,
                owner,
                tarea
            )
            records.append(tasca)
            
        return records