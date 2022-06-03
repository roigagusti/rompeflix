
from classes.Board import Boards
from classes.DataBase import Db



class Task():
    def __init__(self): #Se carga clase instanciando la BD y el Board
        self.b = Boards()
        self.db=Db()

    def create_activity(self, lista_tuplas_de_actividades):

        # Se le pasa un listado con los campos para crear actividad con el formato [(tarea, area, equipo, semana, fecha_plani, y_n, onbsevaciones),(...),(...)]
        # Crea un sticker en Miro, añade la tarea en BD juntamente con el Miro_id y sus coordenadas

        # to_db = [x+tuple(self.b.create_sticker((x[6],str(x[7]),str(x[8])))) for x in lista_tuplas_de_actividades]
        to_db = [x+tuple(self.b.create_sticker(x[6])) for x in lista_tuplas_de_actividades]
        self.db.insert_task_register(to_db)
        return len(to_db)

    def get_date_and_area_coord(self,data,area):
        x = self.db.select_file_mon_board('x',str(data))
        y = self.db.select_file_mon_board('y',str(area))
        z=x[0]+y[0]
        return z

    def create_activities_dateAreaEquipo(self, registro):
        # Formato registro a pasar [('EJECUTIVO ADMINISTRATIVO', 'Piso 02', 'EQUIPO BIM', 1, '14/04/22', 'X', 'test MULTI'),('EJECUTIVO ADMINISTRATIVO', 'Piso 03', 'EQUIPO DE DISEÑO', 1, '13/04/22', 'X', 'test MULTI_2'),('EJECUTIVO ADMINISTRATIVO', 'Piso 01', 'INDUSTRIA ONSITE', 1, '11/04/22', 'X', 'test MULTI_3')]
        #Genera sticker en la posición de area y fecha que le pases, formato. En el color del area indicada

        for x in range(len(registro)):
            y = registro[x] + self.get_date_and_area_coord(registro[x][4], registro[x][1])
            colorEquipo = self.db.get_projectAreaColor(registro[x][2])
            id_sticker = self.b.create_sticker(y[6], float(y[7]), float(y[8]), colorEquipo[0][0])
            registro[x] += tuple(id_sticker)
            self.db.insert_task_register([registro[x]])


    def modify_activity_text(self, widjetId, modification):
        modifiedCol = 'observaciones'
        self.db.modify_activity_register(widjetId, modifiedCol, modification)
        self.b.modify_widjet_text (widjetId, modification)


    def importar_new_activities_form_board(self):

        test = self.db.newGridStickersV2(self.b.board_snap_widgetTypeV2('sticker'))
        grid = self.db.select_file_mon_board_grid()
        fecha = [tuple(grid[x][0] for x in range(len(grid)) if grid[x][2] == test[y][7]) for y in range(len(test))]
        area = [tuple(grid[x][0] for x in range(len(grid)) if grid[x][1] == test[y][6]) for y in range(len(test))]

        gridColor = self.db.get_colorArea()
        equipo = [tuple(gridColor[x][0] for x in range(len(gridColor)) if gridColor[x][1] == test[y][5]) for y in range(len(test))]

        activity = [('tarea',)+area[x]+equipo[x]+('1',)+fecha[x]+('X',)+(test[x][2],)+(test[x][0],)+(test[x][3],)+(test[x][4],)+(test[x][7],)+(test[x][7],) for x in range(len(test))]
        self.db.insert_activity_form_board(activity)

        return len(activity)

    def update_activities_from_board(self):
        pass

    def create_hitos(self, registro):
        # Formato registro a pasar [('EJECUTIVO ADMINISTRATIVO', 'Piso 02', 'EQUIPO BIM', 1, '14/04/22', 'X', 'test MULTI'),('EJECUTIVO ADMINISTRATIVO', 'Piso 03', 'EQUIPO DE DISEÑO', 1, '13/04/22', 'X', 'test MULTI_2'),('EJECUTIVO ADMINISTRATIVO', 'Piso 01', 'INDUSTRIA ONSITE', 1, '11/04/22', 'X', 'test MULTI_3')]
        #Genera sticker en la posición de area y fecha que le pases, formato. En el color del area indicada

        for x in range(len(registro)):
            y = registro[x] + self.get_date_and_area_coord(registro[x][4], registro[x][1])
            colorEquipo = self.db.get_projectAreaColor(registro[x][2])
            id_hito = self.b.create_hito(y[6], float(y[7]), float(y[8]), colorEquipo[0][0])
            registro[x] += tuple(id_hito)
            self.db.insert_task_register([registro[x]])

    def importar_rowcol_form_board(self):

        board_text = self.b.board_snap_widgetTypeV2('text')
        self.db.truncate_table_board_rowcol()
        self.db.insert_snap(board_text)


    def set_initial_grid_dates(self, numCol, valCol, numRow, valRow):
        # valCol = {'1': '2022-05-03', '2': '2022-05-04', '3': '2022-05-05', '4': '2022-05-06'} # valores a meter en cada columna
        # valRow = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'} # valores a meter en cada fila
        # numRow, numCol = ['1', '2','3','4'] #numero columnas y/o filas

        col = self.db.select_file_mon_board_colRowIdMiro()[0]
        row = self.db.select_file_mon_board_colRowIdMiro()[1]
        for x in numCol:
            modifier = (valCol.get(x),col.get('COL'+x))
            self.db.update_grid_values(modifier,'text')
            self.b.modify_widjet_text(modifier[1],modifier[0])
        for x in numRow:
            modifier = (valRow.get(x),row.get('ROW'+x))
            self.db.update_grid_values(modifier,'text')
            self.b.modify_widjet_text(modifier[1],modifier[0])



