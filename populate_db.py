# -*- coding: utf-8 -*-
import json
import psycopg2
import settings

with open("all_atms_info.json") as f:
    atms_json = json.load(f)
f.close()

print(atms_json)

connection = psycopg2.connect(database=settings.DATABASE_NAME, user=settings.DATABASE_USER, password=settings.DATABASE_PASSWORD)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS atm_locations")        
cursor.execute("CREATE TABLE atm_locations(city VARCHAR NOT NULL,addr VARCHAR NOT NULL,whour VARCHAR,coord geometry(POINT,4326))")
cursor.execute("CREATE INDEX atmloc_index ON atm_locations USING GIST(coord)")
connection.commit()

insert_sql = "INSERT INTO atm_locations(city,addr,whour,coord) VALUES(%s,%s,%s,ST_GeomFromText(%s,4326))"
for city in atms_json['atms']:
    for atm in city:
        print(atm['title'], atm['lng'], atm['lat'], atm['addr'])
        coord = "POINT(%s %s)" % (atm['lng'], atm['lat'])
        cursor.execute(insert_sql, (atm['title'], atm['addr'], atm['wtm'], coord))

connection.commit()  
cursor.close()
connection.close()      
