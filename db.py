import mysql.connector
from classes.private import dbCredentials

host,database,user,password,port = dbCredentials()

def connectar(query,type):
    try:
        connection = mysql.connector.connect(user=user,password=password,database=database,host=host,port=port)

        cursor = connection.cursor()
        cursor.execute(query)
        # get all records
        if type == 'select':
            records = cursor.fetchall()
        if type == 'insert':
            connection.commit()
            records = "insertat"
    except mysql.connector.Error as e:
        return False
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
    return records

def dbSelect(taula, select="*"):
    query = "select " + select + " from " + taula
    connexio = connectar(query,"select")
    return connexio

def dbInsert(taula,miid,name,email):
    query = "insert into " + taula + " (miid, name, email) values ('"+ miid +"','"+ name +"','"+ email +"')"
    connexio = connectar(query,"insert")
    return connexio

def dbUpdate(taula,miid,name,email):
    query = "update " + taula + " set name='"+name+"', email='"+email+"' where miid='"+miid+"'"
    connexio = connectar(query,"insert")
    return connexio

#insert = dbInsert("rompeflix_users","43252345235","Marc","marc@011h.com")
#consulta = dbSelect("rompeflix_users")