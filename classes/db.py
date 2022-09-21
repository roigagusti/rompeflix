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

def dbHas(taula, where, columns="*"):
    # taula: string
    # columns: string "columna-A,columnaB,columnaC" (optional, ALL per defecte)
    # where: string "column='valor'" (optional, sense filtre per defecte)
    # columns: string "columna-A,columnaB,columnaC" (optional, ALL per defecte)
    query = "select " + columns + " from " + taula + ' where ' + where
    connexio = connectar(query,"has")
    if connexio > 0:
        answer = True
    else:
        answer = False
    return connexio