# Project 1: Storing Storm Data

## Objectives

1. Install PostgreSQL and make sure you can connect to the database with Python (see below for setup instructions)
2. Create a table to store hurricane data from a CSV file. The file contains the following fields:
    - `fid` - ID for the row
    - `year` - Recorded year
    - `month` - Recorded month
    - `day` - Recorded date
    - `ad_time` - Recorded time in UTC
    - `btid` - Hurricane ID
    - `name` - Name of the hurricane
    - `lat` - Latitude of the recorded location
    - `long` - Longitude of the recorded location
    - `wind_kts` - Wind speed in knots per second
    - `pressure` - Atmospheric pressure of the hurricane
    - `cat` - Hurricane category
    - `basin` - The basin the hurricane is located
    - `shape_leng` - Hurricane shape length
3. Combine `year`, `month`, `day`, and `ad_time` into a single column to store the recorded date and time.
4. Create a user that can perform the following operations on the table:
    - update
    - read
    - insert 
5. Insert the data into the table


## Setup Instructions

1. Download Postgres.app [here](https://postgresapp.com/), open it, and start the database server
	- Default port number is **5432**
	- To test your installation, open your command line application, type ``psql``, and you should be in the PostgreSQL shell
		- Exit ``psql`` by typing ``\q`` and pressing ``Enter``

2. Add the following line to the end of ``~/.bash_profile``

		export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin

	Now, run

		$ source ~/.bash_profile

3. Set up a virtualenv for this project

		$ virtualenv venv-proj1
		$ cd venv-proj1
		$ source bin/activate

4. Install psycopg2

		$ pip3 install psycopg2

5. Launch your Python shell and import the psycopg2 library. Then, run the following code to connect to PostgreSQL and test that everything works as expected. If no errors were returned, then your setup is good to go!

	```python
	import psycopg2
	conn = psycopg2.connect(dbname="postgres", user="postgres")
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE notes(id integer PRIMARY KEY, body text, title text)")
	conn.close()
	```	

6. Install requests

		$ pip3 install requests
