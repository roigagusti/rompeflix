import requests
import json

#user: Agustí
#app: Airtable
class Demo():
    def __init__(self, atid, title, image, cover, video, release, tag, main_style, age, duration, status, quality, directors, staff, description1, description2, description3, season, image_position):
        self.id = atid  
        self.title = title
        self.image =  image
        self.cover = cover
        self.video = video
        self.release_date = release
        self.tag = tag
        self.main_style = main_style
        self.age = age
        self.duration = duration
        self.status = status
        self.quality = quality
        self.directors = directors
        self.staff = staff
        self.description1 = description1
        self.description2 = description2
        self.description3 = description3
        self.season = season
        self.image_position = image_position

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
            if 'description2' in record['fields']:
                description2 = record['fields']['description2']
            else:
                description2 = ''
            if 'description3' in record['fields']:
                description3 = record['fields']['description3']
            else:
                description3 = ''
            demo = Demo(
                record['id'],
                record['fields']['title'],
                record['fields']['main_image'],
                record['fields']['cover_image'],
                record['fields']['video'],
                record['fields']['release_date'],
                record['fields']['tag'],
                record['fields']['main_style'],
                record['fields']['age'],
                record['fields']['duration'],
                record['fields']['status'],
                record['fields']['quality'],
                record['fields']['name (from Directors)'],
                record['fields']['name (from staff)'],
                record['fields']['description1'],
                description2,
                description3,              
                record['fields']['season'],
                record['fields']['main_image_position'],
            )
            records.append(demo)
        return records

    def record(self,id):
        url = 'https://api.airtable.com/v0/'+ self.base_id +'/demodays/' + id
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(url,headers=header)
        record = response.json()
        if 'description2' in record['fields']:
            description2 = record['fields']['description2']
        else:
            description2 = ''
        if 'description3' in record['fields']:
            description3 = record['fields']['description3']
        else:
            description3 = ''
        demo = Demo(
            record['id'],
            record['fields']['title'],
            record['fields']['main_image'],
            record['fields']['cover_image'],
            record['fields']['video'],
            record['fields']['release_date'],
            record['fields']['tag'],
            record['fields']['main_style'],
            record['fields']['age'],
            record['fields']['duration'],
            record['fields']['status'],
            record['fields']['quality'],
            record['fields']['name (from Directors)'],
            record['fields']['name (from staff)'],
            record['fields']['description1'],
            description2,
            description3,
            record['fields']['season'],
            record['fields']['main_image_position']
        )
        return demo
    
    def search(self,parameter,data):
        url = "https://api.airtable.com/v0/"+ self.base_id +"/demodays?filterByFormula={" + parameter + "}='" + data + "'"
        key = 'Bearer '+ self.token
        header = {'Authorization' : key}
        response = requests.get(url,headers=header)
        data = response.json()
        records = []
        for record in data['records']:
            if 'description2' in record['fields']:
                description2 = record['fields']['description2']
            else:
                description2 = ''
            if 'description3' in record['fields']:
                description3 = record['fields']['description3']
            else:
                description3 = ''
            demo = Demo(
                record['id'],
                record['fields']['title'],
                record['fields']['main_image'],
                record['fields']['cover_image'],
                record['fields']['video'],
                record['fields']['release_date'],
                record['fields']['tag'],
                record['fields']['main_style'],
                record['fields']['age'],
                record['fields']['duration'],                
                record['fields']['status'],
                record['fields']['quality'],
                record['fields']['name (from Directors)'],
                record['fields']['name (from staff)'],
                record['fields']['description1'],
                description2,
                description3,
                record['fields']['season'],
                record['fields']['main_image_position']
            )
            records.append(demo)
        return records