import mysql.connector
import json
from flask import Flask

app = Flask(__name__)

# keep our old route
@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route("/goodbye")
def goodbye():
    return {"data": "So long, and thanks for all the fish!"}

# a new route to query the `widgets` table in our application DB
@app.route('/widgets')
def get_widgets():
    # connect to the database
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )

    # now query the database
    # you don't need to worry about how this code works!
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM widgets")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()

    # once we have the data, we can return it to the client
    return json.dumps(json_data)

# a new route to create the database and table to be queried
@app.route('/initdb')
def db_init():
    # connect to the database manager
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )

    # create the database
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    # connect to the database
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )

    # create the table
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    # return a string to confirm it worked
    return 'init database'

# this section allows us to run the app with `python app.py`
# on the command line
if __name__ == "__main__":
    app.run(host ='0.0.0.0')