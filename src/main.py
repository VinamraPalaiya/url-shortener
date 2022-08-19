import os
from typing import Union
from flask import Flask, redirect, Response, request, render_template
import mysql.connector
import hashlib, base64

# Create the flask application 
app = Flask(__name__)

# Configuration required to connect to MYSQL db
# edit user and password parameters for access to MYSQL db
config = {'host': 'localhost', 'user': 'root', 'passwd': 'password', 'auth_plugin': 'mysql_native_password', 'database': 'mydatabases'}


def initialize_database() -> None:
    """
    Function to check for and create the required MYSQL Database and MYSQL Tables 
    for storing and fetching urls
    @param               : None
    @type                : None
    @return              : None
    @return_type         : None
    """
    
    # create a connection to database using mysql-connector
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()
    
    # check if 'mydatabases' exists, create one if not
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabases")
    mydb = mysql.connector.connect(**config)
    mycursor = mydb.cursor()
    
    # Check if urls table exists
    mycursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'mydatabases' AND table_name = 'urls'")
    
    # If the urls table doesn't exist, create one
    if mycursor.fetchone() is None:
        # Create urls table with shortlink of fixed length 7 and long url as columns
        # with short link as the primary key 
        mycursor.execute("CREATE TABLE urls (id VARCHAR(7) PRIMARY KEY, url VARCHAR(2048))")


def generate_id_from_url(url: str) -> str:
    """
    Function to generate hash id of fixed length 7 from long url 
    using MD5 hash function and base64 encoding 
    @param url           : long url 
    @type  url           : str
    @return              : short id
    @return_type         : str
    """
    md5 = hashlib.md5(url.encode()).digest()
    b64 = base64.b64encode(md5)
    full_id = str(b64)[2:-3]
    # taking the first 7 characters of the base64 encoded no.
    id = full_id[:7]
    return id

def get_url(id: str) -> Union[str, None]:
    """
    Function to return the Long Url for a given short id 
    if short id exists in Database otherwise return None
    @param id            : short id
    @type                : str
    @return              : either long url or None
    @return_type         : either str or None
    """

    # Connect to the database
    with mysql.connector.connect(**config) as mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT url FROM urls WHERE id = %s", (id,))
        data = mycursor.fetchone()
        # If the url exists, return it. Otherwise, return None
        if data:
            return data[0]
        return None


def store_id_url(id: str, url: str) -> str:
    """
    Function to insert a short id-long Url, key-value pair 
    and commit changes to the database when a new url write occurs
    @param               : short id and long url
    @type                : str and str
    @return              : short id
    @return_type         : str
    """
    # Connect to the database
    with mysql.connector.connect(**config) as mydb:
        mycursor = mydb.cursor()        
        # sql command for insert
        cmd = "INSERT INTO urls(id, url) VALUES (%s, %s)"
        # values to be inserted
        values = (id,url)
        mycursor.execute(cmd,values)
        # commit changes to db to persist
        mydb.commit()
        # Return the id of the new url
        return id


def exists_id(id: str) -> bool:
    """
    Function to return True or False 
    depending on whether a short id exists in DB or not
    @param               : short id
    @type                : str
    @return              : bool flag
    @return_type         : bool
    """
    # Connect to the database
    with mysql.connector.connect(**config) as mydb:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT id FROM urls WHERE id = %s', (id,))
        
        # If the url exists, return True. Otherwise, return False
        query_result = mycursor.fetchone()
        if query_result:
            return True
        else:
            return False


def shorten_url(url: str) -> str:
    """
    Function to check whether a long url exists in db and return its complete short link url
    otherwise generate short link url, add to DB and return newly generated short link
    @param               : long url
    @type                : str
    @return              : complete short URL
    @return_type         : str
    """
    id = generate_id_from_url(url)
    id_exists = exists_id(id)
    
    if id_exists == False:
        id = store_id_url(str(id),str(url))
    
    # Return the shortened url
    return request.base_url + '?id=' + str(id)
    

# Create the home page route 
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        """
        Get request mapping a short url link 
        to original long url link and redirecting to it
        """
        # Check if the id parameter exists in Short Link
        id = request.args.get('id')
        if id:
            # Get the url from the database.
            url = get_url(str(id))
            # If the url exists, redirect to it.
            if url:
                return redirect(url)    
            # If the id is invalid, return a 404 error
            return Response('<h1>Invalid URL</h1>', status=404)
        else:
            # If the id parameter doesn't exist, return just the home page
            return render_template('index.html')
    
    elif request.method == 'POST':
        """
        Post request mapping a long url link to short link url
        """
        # Check if the url parameter exists
        url = request.form['url']
        if url:
            # Shorten the url and return it
            shortened_url = shorten_url(url.strip())
            return render_template('index.html', url=shortened_url)
        else:
            # If the url parameter doesn't exist, return just the home page
            return render_template('index.html')
    
def main():
    # Call to check and if required create MYSQL database or table
    initialize_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()
