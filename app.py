#use Flask to render a template, redirect to another URL and create a URL
from flask import Flask,render_template,redirect,url_for

#use PyMongo to interact w/ MongoDB
from flask_pymongo import PyMongo

#Will convert from Jupyter notebook to Python
import scraping

#set up Flask
app=Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

#create app routes
@app.route("/")
#links our web app to the code that powers it
def index():
    #uses PyMongo to find the 'mars' collection in DB and assign the path 'mars'
    mars=mongo.db.mars.find_one()
    #tells Flask to return HTML template using index.html file and tells python to use the 'mars' collection
    return render_template("index.html",mars=mars)

#add scraping route/button
@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    mars_data=scraping.scrape_all()
    mars.replace_one({},mars_data,upsert=True)
    return redirect('/',code=302)

#tell Flask to run
if __name__=="__main__":
    app.run()    
