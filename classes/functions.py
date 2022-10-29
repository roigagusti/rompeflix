import time
import datetime
from sqlalchemy import create_engine, select, MetaData, Table

def dateToYear(numero):
    string = str(numero)
    date = datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")
    year = date.strftime("%B %Y")
    return year

def connectRT():
    host = 'dev-rompetechos-cluster.cluster-cibamr7b9vqj.eu-central-1.rds.amazonaws.com'
    user = 'dev_rt_admin'
    password = 'rtDevBuPla3ADM!'
    port = '3306'
    database = 'dev_rt_support'
    
    database_uri = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
    engine = create_engine(database_uri, echo=True, future=True)
    return engine

def get_table(table):
    metadata = MetaData()
    engine = connectRT()
    table = Table(table, metadata, autoload=True, autoload_with=engine)
    return table