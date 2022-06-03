import requests
import json

#user: Agustí
#app: Airtable
class Demo():
    def __init__(self, title, image, video, release, tag, main_style, age, duration, status):    
        self.title = title
        self.image =  image
        self.video = video
        self.release_date = release
        self.tag = tag
        self.main_style = main_style
        self.age = age
        self.duration = duration
        self.status = status

class Airtable():
    def __init__(self):
        self.token = 'keyVBM9rXFpJNDEIU'
        self.base_id = 'applVLtXI9jhnWeIB'

    def list(self,maxrecords,formula,tag):
        url = 'https://api.airtable.com/v0/applVLtXI9jhnWeIB/demodays'
        numero = '?maxRecords='+str(maxrecords)
        grid = '&view=public'
        filtre = "&filterByFormula={"+formula+"}='"+tag+"'"
        sort = '&sort%5B0%5D%5Bfield%5D=release_date&sort%5B0%5D%5Bdirection%5D=desc'
        rest = url+numero+grid+filtre+sort
        
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(rest,headers=header)
        data = response.json()
        records = []
        for record in data['records']:
            demo = Demo(record['fields']['title'],record['fields']['image'],record['fields']['video'],record['fields']['release_date'],record['fields']['tag'],record['fields']['main_style'],record['fields']['age'],record['fields']['duration'],record['fields']['status'])
            records.append(demo)
        return records

    def record(self,id):
        url = 'https://api.airtable.com/v0/'+ self.base_id +'/demodays/' + id
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(url,headers=header)
        data = response.json()
        demo = Demo(data['fields']['title'],data['fields']['image'],data['fields']['video'],data['fields']['release_date'],data['fields']['tag'],data['fields']['main_style'],data['fields']['age'],data['fields']['duration'],data['fields']['status'])
        return demo