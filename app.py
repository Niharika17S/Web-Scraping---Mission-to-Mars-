from flask import Flask, render_template
import scrape
import pymongo

app = Flask(__name__)

@app.route("/")
    return render_template("index.html", dict = mars_dict)

@app.route("/scrape")
def scrape():
    return render_template
    marscrape = scrape.scrape()