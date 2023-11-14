import requests as req

import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('./starwars.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS starwars (
	name text NOT NULL,
	model text NOT NULL,
    manufacturer text NOT NULL,
	passengers INTEGER NOT NULL,
    created text NOT NULL,
    url text NOT NULL,
	PRIMARY KEY (name ASC)
) """)

print("Table created successfully")

cursor.execute("DELETE FROM starwars ")

# Inserting data to model 

def star_war_data():
    
    page = 1 
    temp_url = "https://swapi.dev/api/starships/?page={page}"

    data = []
    url = temp_url.format(page=page)
    res = req.get(url)
    res = res.json()
    while len(res.get('results',[])) > 0 :
        results = res['results']
        for rr in results:
            t = {"name": rr["name"] , "model": rr["model"], "manufacturer": rr["manufacturer"] , "passengers": rr["passengers"], "created": rr["created"], "url": rr["url"] }
            data.append(t)
        page+=1 
        url = temp_url.format(page=page)
        res = req.get(url)
        
        res = res.json()
    #print(data)
    
    return data 

data = star_war_data()
print(f"Number of records inserted are : {len(data)}")
print("inserting data to starwars")
cursor.executemany('''
        INSERT INTO starwars (name, model, manufacturer, passengers, created, url) VALUES (:name, :model, :manufacturer, :passengers, :created, :url)
    ''', data)

print("insertion data to starwars completed")


conn.commit()

cursor.execute("SELECT DISTINCT manufacturer FROM starwars")
manufacturers = [row[0] for row in cursor.fetchall()]
print("Sample data")
print(manufacturers)
#Closing the connection
conn.close()
