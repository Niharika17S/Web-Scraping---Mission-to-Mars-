from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("index.html", dict = mars_dict)

@app.route("/scrape")
def scrape():
    
    marscrape = scrape.scrape()
    mongo.db.collection.insert_one(mission_mars)
    
if __name__ == "__main__":
    app.run(debug=True)    