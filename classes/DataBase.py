import mysql.connector

class Db():
    def __conectr_bd(self):

        self.mydb = None
        try:
            self.mydb = mysql.connector.connect(
                host = "dev-rompetechos-cluster.cluster-cibamr7b9vqj.eu-central-1.rds.amazonaws.com",
                user = "dev_rt_admin",
                password = "rtDevBuPla3ADM!")

        except:
            print('Error al connectar a BD')

        return self.mydb

    def insert_task_register(self,val):
        # le pasas una lista con tuplas de todos los regisgtros de los campos (tarea, area, equipo, semana, y_n, observaciones, id_miro, x_miro, y_miro)

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`file_mon` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL,NULL)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')


    def select_file_mon(self, col, where=None):
        # le pasas las columnas que quieres que te muestre como string 'tarea, area, equipo'. El where tmb como str
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            if where != None:
                self.mycursor.execute(f"SELECT {col} FROM `dev_rt_playground`.`file_mon` WHERE {where}")
                result = self.mycursor.fetchall()
            else:
                self.mycursor.execute(f"SELECT {col} FROM `dev_rt_playground`.`file_mon`")
                result = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result


    def file_mon_process_reeng(self, col, where=None):
        # le pasas las columnas que quieres que te muestre como string 'tarea, area, equipo'. El where tmb como str
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            if where != None:
                self.mycursor.execute(f"SELECT {col} FROM `dev_rt_playground`.`file_mon_process_reeng` WHERE {where}")
                result = self.mycursor.fetchall()
            else:
                self.mycursor.execute(f"SELECT {col} FROM `dev_rt_playground`.`file_mon_process_reeng`")
                result = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result


    def insert_snap(self,val):
        # le pasas una lista con tuplas de todos los regisgtros de los campos (id_miro,widjet_type,text,x,y,color,gridrow,gridcol)

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`file_mon_board` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')

    def select_file_mon_board(self, col, text_colOrRow):
        # le pasas las columnas que quieres que te muestre como string 'tarea, area, equipo'. El where tmb como str
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f"SELECT {col} FROM dev_rt_playground.file_mon_board WHERE text = '{text_colOrRow}'")
            result = self.mycursor.fetchall()


        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def modify_activity_register(self, widjetId, modifiedCol, modification):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f" UPDATE dev_rt_playground.file_mon SET {modifiedCol} = '{modification}' WHERE id_miro = {widjetId}")
            self.mydb.commit()


        finally:
            self.mydb.close()
            # print('Desconectado de BD')

    def update_activity_register_from_web(self, DBId, modifiedCol, modification):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f" UPDATE dev_rt_playground.file_mon SET {modifiedCol} = '{modification}' WHERE id = {DBId}")
            self.mydb.commit()


        finally:
            self.mydb.close()



    def get_projectAreaColor(self, area):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f"SELECT color FROM dev_rt_playground.tipo_area_file_mon WHERE name = '{area}'")
            result = self.mycursor.fetchall()


        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def newActivities(self):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute( 'SELECT id_miro FROM dev_rt_playground.file_mon')
            result = self.mycursor.fetchall()
            list_activities = [result[x][0] for x in range(len(result)) if result[x][0] != None]

            self.mycursor.execute( "SELECT id_miro FROM dev_rt_playground.file_mon_board WHERE widjet_type = 'sticker'")
            result2 = self.mycursor.fetchall()
            list_stickers = [result2[x][0] for x in range(len(result2)) if result2[x][0] != None]

            new_stickers = [x for x in list_stickers if x not in list_activities]


            self.mycursor.execute( f"SELECT * FROM dev_rt_playground.file_mon_board WHERE  id_miro in {tuple(new_stickers)}" )
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def select_file_mon_board_grid(self):
        # le pasas las columnas que quieres que te muestre como string 'tarea, area, equipo'. El where tmb como str
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT text, grid_row, grid_col FROM dev_rt_playground.file_mon_board WHERE widjet_type = 'text'")
            result = self.mycursor.fetchall()


        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def newGridRowColm(self, snap_list):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute( "SELECT id_miro FROM dev_rt_playground.file_mon_board WHERE widjet_type = 'text'")
            result2 = self.mycursor.fetchall()
            list_stickers = [result2[x][0] for x in range(len(result2)) if result2[x][0] != None]

            new_stickers = [x for x in snap_list if x[0] not in list_stickers]

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return new_stickers

    def get_colorArea(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT name,color FROM dev_rt_playground.tipo_area_file_mon")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def insert_activity_form_board(self,val):
        # le pasas una lista con tuplas de todos los regisgtros de los campos (tarea, area, equipo, semana, y_n, observaciones, id_miro, x_miro, y_miro)

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`file_mon` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')

    def newGridStickersV2(self, snap_list):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute( "SELECT id_miro FROM dev_rt_playground.file_mon")
            result2 = self.mycursor.fetchall()
            list_activities_existentes = [result2[x][0] for x in range(len(result2)) if result2[x][0] != None]

            new_activities = [x for x in snap_list if x[0] not in list_activities_existentes]

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return new_activities

    def activities_in_db(self):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute( "SELECT * FROM dev_rt_playground.file_mon WHERE id_miro IS NOT NULL")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')
        return result

    def truncate_table_board_rowcol(self):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            self.mycursor.execute("TRUNCATE TABLE dev_rt_playground.file_mon_board")
            self.mydb.commit()

        finally:
            self.mydb.close()


    def update_grid_values(self,val,field):
        # le pasas una lista con tuplas de todos los regisgtros de los campos (id_miro,widjet_type,text,x,y,color,gridrow,gridcol)
        # val = ('valor a updatear','id_miro')

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = (f"UPDATE `dev_rt_playground`.`file_mon_board` SET `{field}`= %s WHERE id_miro = %s")

            self.mycursor.execute(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')


    def select_file_mon_board_colRowIdMiro(self):
            # le pasas las columnas que quieres que te muestre como string 'tarea, area, equipo'. El where tmb como str
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT text, id_miro FROM dev_rt_playground.file_mon_board WHERE text LIKE 'COL%'")
            result = self.mycursor.fetchall()
            self.mycursor.execute("SELECT text, id_miro FROM dev_rt_playground.file_mon_board WHERE text LIKE 'ROW%'")
            result2 = self.mycursor.fetchall()

        finally:
            self.mydb.close()
            # print('Desconectado de BD')

        result = dict(result)
        result2 = dict(result2)

        return result, result2

    def get_zones(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT nombre FROM dev_rt_playground.tipo_zona_file_mon")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result


    def get_tareas(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT nombre FROM dev_rt_playground.tipo_tarea_file_mon")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result

    def get_racks_inregistre(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT * FROM dev_rt_playground.registro_camiones")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result

    def get_racks_inregistre_byrack(self,rack):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f"SELECT * FROM dev_rt_playground.registro_camiones WHERE rack_id = {rack}")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result

    def get_racks_tipo(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT * FROM dev_rt_playground.tipo_real_rack")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result


    def get_camions_temp(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT * FROM dev_rt_playground.registro_camiones_temporal")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result


    def insert_camion_temp(self,val):
        # lisat de tupla

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`registro_camiones_temporal` VALUES (NULL,%s,%s,%s,%s)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()

    def truncate_table_camiones_temp(self):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            self.mycursor.execute("TRUNCATE TABLE dev_rt_playground.registro_camiones_temporal")
            self.mydb.commit()

        finally:
            self.mydb.close()

    def delete_panel_id_temp(self,panelid):
        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            self.mycursor.execute(f"DELETE FROM dev_rt_playground.registro_camiones_temporal WHERE id ='{panelid}'")
            self.mydb.commit()

        finally:
            self.mydb.close()

    def insert_camion(self,val):
        # lisat de tupla

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`registro_camiones` VALUES (NULL,%s,%s,%s,%s)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()



    def get_camions_temp_to_save(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT matricula, rack_id, eu_ins, fecha_reg FROM dev_rt_playground.registro_camiones_temporal")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result

    def insert_bom(self,val):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:
            sql = "INSERT INTO `dev_rt_playground`.`registrobom` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL)"

            self.mycursor.executemany(sql, val)
            self.mydb.commit()

        finally:
            self.mydb.close()


    def get_bom(self):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute("SELECT * FROM dev_rt_playground.registrobom")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result

    def get_bom_eu(self,EU_tuple):

        self.mydb = self.__conectr_bd()
        self.mycursor = self.mydb.cursor()
        try:

            self.mycursor.execute(f"SELECT * FROM dev_rt_playground.registrobom WHERE execution_unit_id in {EU_tuple} AND description LIKE 'Related material%' ")
            result = self.mycursor.fetchall()

        finally:
            self.mydb.close()

        return result
