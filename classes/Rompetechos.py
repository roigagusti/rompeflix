from classes.functions import connectRT, get_table
from sqlalchemy.sql import select

class Demo():
    def __init__(self, atid, title):
        self.atid = atid
        self.title = title

# demos = get_table('rompeflix_media')
# cols = demos.c
# engine = connectRT()

# with engine.connect() as conn:
#     query = (
#         select([cols.atid, cols.title, cols.created])
#             .order_by(cols.created)
#             .limit(10)
#     )
#     for row in conn.execute(query):
#         print(row)
        





class Rompeflix():
    def __init__(self):
        self.table = 'rompeflix_media'

    def list(self,maxrecords):
        #list(4,'slider_main','Yes')
        demos = get_table(self.table)
        cols = demos.c
        engine = connectRT()
        records = []
        with engine.connect() as conn:
            query = (
                select([cols.atid, cols.title, cols.created])
                    .order_by(cols.created)
                    .limit(maxrecords)
            )
            for row in conn.execute(query):
                demo = Demo(
                    row['atid'],
                    row['title']
                )
                records.append(demo)
        return records

    def record(self,id):
        pass
        #return demo
    
    def search(self,parameter,data):
        pass
        #return records