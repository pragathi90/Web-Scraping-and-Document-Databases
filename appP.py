# Flask application
# Create a route called /scrape that will import your scrape_mars.py script and call your  scrape function

# Dependencies
import pymongo
import scrape_marsP
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import sys


# Create flask app
app = Flask(__name__)


#mongo = PyMongo(app, uri="mongodb://localhost:27017/Mission_To_Mars_App")
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars_App"
mongo = PyMongo(app)


# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route("/")
def index():

    print("MONGO")
    # Find one record of data from the mongo database
    mars_information = mongo.db.mars_db.find_one()

    print("My HTML")
    #marsdata = list(db.marsdata.find())
    return render_template("index.html", mars_data=mars_information)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    
    mars_data = scrape_marsP.get_news()
    mars_data = scrape_marsP.get_featured_image()
    mars_data = scrape_marsP.get_facts()
    mars_data = scrape_marsP.get_latest_weather()
    mars_data = scrape_marsP.get_hemispheres()
    mongo.db.mars_db.update({}, mars_data, upsert=True)
    
    print("REDIRECT")
    #return redirect('http://localhost:5000/', code=302)
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)