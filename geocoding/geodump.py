import sqlite3
import json
import codecs

# Open the file handler to write the data INTO
# It will truncate all the existing data
file_handler = codecs.open('where.js', 'w', 'utf-8')
file_handler.write('myData=[\n')
count = 0

# Open the database connection
conn = sqlite3.connect('geodata.sqlite')
cursor = conn.cursor()

# Get the data from the table LOCATIONS
cursor.execute('SELECT geodata FROM LOCATIONS')
rows = cursor.fetchall()

if rows is None:
    print('No data in the database, run the geoload.py first')
    exit()

for row in rows:
    data = str(row[0].decode())
    try:
        js = json.loads(data)
    except:
        print('Failed to load JSON from locations')
        continue

    if 'status' not in js or js['status'] != 'OK' and js['status'] == 'ZERO_RESULTS':
        continue

    print(json.dumps(js, indent=2))
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']

    if lat == 0 or lng == 0:
        continue

    address = js['results'][0]['formatted_address']
    address = address.replace("'", "")
    try:
        print(address, lat, lng)
        count += 1

        if count > 1:
            file_handler.write(",\n")

        output = "["+str(lat)+","+str(lng)+", '"+address+"']"
        file_handler.write(output)

    except:
        continue


file_handler.write("\n];\n")
cursor.close()
file_handler.close()
