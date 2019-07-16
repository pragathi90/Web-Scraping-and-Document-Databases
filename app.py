# Flask application
# Create a route called /scrape that will import your scrape_mars.py script and call your  scrape function

# Dependencies
import pymongo
import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# Create flask app
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdata")

# Connect to MongoDB

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it
db = client.marsdataDB
collection = db.marsdata

marsdata = list(db.marsdata.find())
# print(marsdata)




# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():

    # Find one record of data from the mongo database
    marsdata = db.marsdata.find_one()


    #marsdata = list(db.marsdata.find())
    return render_template('index.html', marsdata=marsdata)

# Create route called /scrape
@app.route('/scrape')
def scrape():

    # Run the scrape function
    marsdata = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.marsdata.update({}, marsdata, upsert=True)
   
    #mongo.db.collection.update({}, costa_data, upsert=True)
    return redirect('http://localhost:5000/', code=302)
    #return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)




