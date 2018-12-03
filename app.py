from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def home():
    mars_dictionary = mongo.db.mars_dict.find_one()
    return render_template("index.html", dict = mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mars_dict.update({},
     mars_data, upsert=True)
    return 

if __name__ == "__main__":
    app.run(debug=True)    