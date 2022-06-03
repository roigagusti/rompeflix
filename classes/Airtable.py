from Flask import request



class Airtable():
    def __init__(self):
        self.token = 'keyVBM9rXFpJNDEIU' #user: Agustí
        self.base_id = 'tblKiO47iSnjOFGle' #taula: Demodays

    def record(self,id):
        url = 'https://api.airtable.com/v0/' + self.base_id + '/Demodays/' + id
        header = {'Authorization': 'Bearer ' + self.token}
        response = request.get(url,header)
        data = response
        return data