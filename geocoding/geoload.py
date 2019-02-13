import urllib.request, urllib.parse, urllib.error
import ssl
import json
import sqlite3
import time

google_api = False

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Create the database
connection = sqlite3.connect('geodata.sqlite')
cursor = connection.cursor()

cursor.executescript(''' CREATE TABLE IF NOT EXISTS Locations(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    address TEXT UNIQUE,
    geodata TEXT
    );''')

# Open the where.data file
file_handler = open('where.data', 'r')

count = 0
address_count = 298

for address in file_handler:
    address = address.rstrip()
    count += 1

    # Check in the db first
    cursor.execute('SELECT address from locations where address = ? ', (memoryview(address.encode()),))
    row = cursor.fetchone()
    if row is not None:
        print('Found address {} in database'.format(address))
        continue

    params = dict()
    # Get the data from the webservices
    if count < address_count:
        params['key'] = 42
        params['address'] = address

        url = 'http://py4e-data.dr-chuck.net/json?' + urllib.parse.urlencode(params)
        print(url)
    else:
        params['key'] = 'AIzaSyDX9HxA40RAn07l9kAwLYvkxAKX1oCsg-8'
        params['address'] = address
        url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.parse.urlencode(params)
        print('Retrieving from Google API...')

    # Get the data from the server
    response = urllib.request.urlopen(url, context=ctx).read().decode()
    print('Retrieved', len(response), 'characters', response[:20].replace('\n', ' '))

    # Load the json response
    try:
        json_response = json.loads(response)
    except:
        print('Failed to parse json')
        continue

    if 'status' not in json_response or json_response['status'] != 'OK' and json_response['status'] != 'ZERO_RESULTS':
        print('==== Failed to Retrieve data ===== ')
        break

    # Populate the table
    print(response)


    if count % 10 == 0:
        print('Pausing for 5 seconds....')
        time.sleep(5)

    cursor.execute('INSERT INTO LOCATIONS(address, geodata) VALUES (? ,?)',
     (memoryview(address.encode()), memoryview(response.encode())))
    connection.commit()

file_handler.close()
connection.close()
