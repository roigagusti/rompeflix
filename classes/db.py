import mysql.connector
from classes.private import dbCredentials

host,database,user,password,port = dbCredentials()
#dbprova = dbInsert('rompeflix_users','miid,name,email',"'"+rtid+"','"+name+"','"+email+"'")
#dbprova = dbSelect('rompeflix_users','name,email',limit=2,offset=3)
#dbprova = dbUpdate('rompeflix_users',"name='"+name+"',email='"+email+"'","miid='gsfdgdsg'")

def connectar(query,type):
    try:
        connection = mysql.connector.connect(user=user,password=password,database=database,host=host,port=port)

        cursor = connection.cursor()
        cursor.execute(query)
        # get all records
        if type == 'insert':
            connection.commit()
            records = cursor.rowcount # files insertades
        if type == 'selectall':
            records = cursor.fetchall()
        if type == 'selectone':
            records = cursor.fetchone()
        if type == 'has':
            records = cursor.rowcount
    except mysql.connector.Error as e:
        return False
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
    return records

def dbInsert(taula,columns,values):
    # taula: string
    # columns: string "columna-A,columnaB,columnaC"
    # values: string "'valor1','valor2','valor3'"
    query = "insert into " + taula + " (" + columns + ") values (" + values + ")"
    connexio = connectar(query,"insert")
    return connexio
    
def dbSelect(taula, columns="*", where=0, like=0, orderby=0, limit=0, offset=0, fetchone=False):
    # taula: string
    # columns: string "columna-A,columnaB,columnaC" (optional, ALL per defecte)
    # where: string "column='valor'" (optional, sense filtre per defecte)
    # like: string "'%way%'"
    # orderby: string "column ASC/DESC" (optional, sense ordre per defecte)
    # limit: int (optional, sense limit per defecte)
    # offset: int (optional, sense offset per defecte)
    # fetchone: retorna només la primera fila (optional, FALSE per defecte)
    query = "select " + columns + " from " + taula
    if where != 0:
        query = query + ' where ' + where
    if like != 0:
        query = query + ' like ' + like
    if orderby != 0:
        query = query + ' order by ' + orderby
    if limit != 0:
        query = query + ' limit ' + str(limit)
        if offset != 0:
            query = query + ' offset ' + str(offset)
    if fetchone == False:
        connexio = connectar(query,"selectall")
    else:
        connexio = connectar(query,"selectone")
    return connexio

def dbUpdate(taula,values,where):
    # taula: string
    # values: string "column1 = 'value1', column2= 'value2'""
    # where: string "column='valor'"
    query = "update " + taula + " set " + values + " where " + where
    connexio = connectar(query,"insert")
    return connexio

def dbHas(taula, where):
    # taula: string
    # columns: string "columna-A,columnaB,columnaC" (optional, ALL per defecte)
    # where: string "column='valor'" (optional, sense filtre per defecte)
    # columns: string "columna-A,columnaB,columnaC" (optional, ALL per defecte)
    contact = dbSelect(taula,where=where)
    connexio = len(contact)
    if connexio > 0:
        answer = True
    else:
        answer = False
    return answer


class Demo():
    def __init__(self, atid, title, image, cover, video, release, status, staff, description1, description2, description3, image_position, category, area):
        self.id = atid  
        self.title = title
        self.image =  image
        self.cover = cover
        self.video = video
        self.release_date = release
        self.status = status
        self.staff = staff
        self.description1 = description1
        self.description2 = description2
        self.description3 = description3
        self.image_position = image_position
        self.category = category
        self.area = area

class Rompetechos():
    def __init__(self,tabla):
        self.tabla = tabla

    def list(self,maxrecords,formula=0,tag=0):
        columns = "atid,title,main_image,cover_image,video,release_date,estat,staff,main_image_position,description1,description2,description3,category,area,release_date"
        if formula != 0 and tag != 0:
            filtre = "%s='%s'" % (formula,tag)
        else:
            filtre = 0
        data = dbSelect(self.tabla,columns=columns,where=filtre,limit=maxrecords,orderby="release_date DESC")
        records = []
        if data != False:
            for record in data:
                atid = record[0]
                title = record[1]
                main_image = record[2]
                cover_image = record[3]
                video = record[4]
                release_date = record[5]
                estat = record[6]
                staff = record[7]
                main_image_position = record[8]
                description1 = record[9]
                description2 = record[10]
                description3 = record[11]
                category = record[12]
                area = record[13]
                demo = Demo(
                    atid,
                    title,
                    main_image,
                    cover_image,
                    video,
                    release_date,
                    estat,
                    staff,
                    description1,
                    description2,
                    description3,
                    main_image_position,
                    category,
                    area
                )
                records.append(demo)
        else:
            records = ''
        return records

    def record(self,atid):
        columns = "atid,title,main_image,cover_image,video,release_date,estat,staff,main_image_position,description1,description2,description3,category,area"
        filtre = "%s='%s'" % ('atid',atid)
        data = dbSelect(self.tabla,columns=columns,where=filtre,limit=1)
        singleData = data[0]

        atid = singleData[0]
        title = singleData[1]
        main_image = singleData[2]
        cover_image = singleData[3]
        video = singleData[4]
        release_date = singleData[5]
        estat = singleData[6]
        staff = singleData[7]
        main_image_position = singleData[8]
        description1 = singleData[9]
        description2 = singleData[10]
        description3 = singleData[11]
        category = singleData[12]
        area = singleData[13]
        demo = Demo(
            atid,
            title,
            main_image,
            cover_image,
            video,
            release_date,
            estat,
            staff,
            description1,
            description2,
            description3,
            main_image_position,
            category,
            area
        )
        return demo
    
    def search(self,parameter,data):
        columns = "atid,title,main_image,cover_image,video,release_date,estat,staff,main_image_position,description1,description2,description3,category,area"
        filtre = "%s='%s'" % (parameter,data)
        data = dbSelect(self.tabla,columns=columns,where=filtre)
        records = []
        for record in data:
            atid = record[0]
            title = record[1]
            main_image = record[2]
            cover_image = record[3]
            video = record[4]
            release_date = record[5]
            estat = record[6]
            staff = record[7]
            main_image_position = record[8]
            description1 = record[9]
            description2 = record[10]
            description3 = record[11]
            category = record[12]
            area = record[13]
            demo = Demo(
                atid,
                title,
                main_image,
                cover_image,
                video,
                release_date,
                estat,
                staff,
                description1,
                description2,
                description3,
                main_image_position,
                category,
                area
            )
            records.append(demo)
        return records