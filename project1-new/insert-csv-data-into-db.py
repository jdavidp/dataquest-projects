import csv
import psycopg2
import requests
from datetime import datetime

conn = psycopg2.connect(dbname='postgres', user='postgres')
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE hurricanes;

    CREATE TABLE hurricanes (
        fid integer,
        recorded_datetime timestamp,
        btid smallint,
        storm_name varchar(25),
        latitude decimal(5, 2),
        longitude decimal(5, 2),
        wind_speed_in_knots smallint,
        pressure smallint,
        category char(2),
        basin varchar(25),
        shape_length decimal(8, 6)
    );

    DROP GROUP IF EXISTS basic_analysts;
    CREATE GROUP basic_analysts WITH NOLOGIN;
    REVOKE ALL ON hurricanes FROM basic_analysts;
    GRANT SELECT ON hurricanes TO basic_analysts;
    DROP USER IF EXISTS john;
    CREATE USER john WITH PASSWORD 'johns_strong_password' IN GROUP basic_analysts;
    
    DROP GROUP IF EXISTS super_analysts;
    CREATE GROUP super_analysts WITH NOLOGIN;
    REVOKE ALL ON hurricanes FROM super_analysts;
    GRANT SELECT, INSERT, UPDATE ON hurricanes TO super_analysts;
    DROP USER IF EXISTS bob;
    CREATE USER bob WITH PASSWORD 'bobs_strong_password' IN GROUP super_analysts;
""")

CSV_URL = 'https://dq-content.s3.amazonaws.com/251/storm_data.csv'
values = []

with requests.get(CSV_URL, stream=True) as response:
    # Set up a generator, skip empty lines
    lines = (line.decode() for line in response.iter_lines() if line)

    # Skip the header
    next(lines)

    # Convert each line into a list
    for row in csv.reader(lines):
        fid = row[0]
        year = row[1]
        month = row[2]
        day = row[3]
        hour = row[4][:-1][:2]
        minute = row[4][:-1][2:]
        recorded_datetime = datetime.strptime(year + '-' + month + '-' + day + ' ' + hour + ':' + minute,
                                              '%Y-%m-%d %H:%M')
        btid = row[5]
        storm_name = row[6]
        latitude = row[7]
        longitude = row[8]
        wind_speed_in_knots = row[9]
        pressure = row[10]
        category = row[11]
        basin = row[12]
        shape_length = row[13]

        # We call decode() to convert bytes->string, so we can append to the list
        values.append(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
            fid, recorded_datetime, btid, storm_name, latitude, longitude, wind_speed_in_knots,
            pressure, category, basin, shape_length)).decode('utf-8'))

values_clause = ','.join(values)
cursor.execute("INSERT INTO hurricanes VALUES " + values_clause)
conn.commit()
