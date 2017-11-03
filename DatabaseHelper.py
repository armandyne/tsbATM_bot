# -*- coding: utf-8 -*-
import psycopg2

class DatabaseHelper:
    def __init__(self, db, user, passw):
        self.connection = psycopg2.connect(database=db, user=user, password=passw)
        self.cursor = self.connection.cursor()
    
    def __del_(self):
        self.cursor.close()
        self.connection.close()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def select_atms(self, longitude, latitude, distance = 400):
        select_sql = '''select t.addr, t.whour, ST_X(t.coord) as lng, ST_Y(t.coord) as lat,
        round(ST_Distance(ST_Transform(t.coord, 26986), ST_Transform(ST_GeomFromText(%s,4326), 26986))) as distance
        from atm_locations t
        where round(ST_Distance(ST_Transform(t.coord, 26986), 
                    ST_Transform(ST_GeomFromText(%s,4326), 26986))) <= %s
        order by distance'''

        location_wkt = "POINT(%s %s)" % (longitude, latitude)        
        self.cursor.execute(select_sql, (location_wkt,location_wkt,distance))
        return self.cursor.fetchall()  