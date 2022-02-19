
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request

from datetime import date as my_date
import datetime

import soccer_scraper, soccer_standings, cup_standings

import os, random

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("home.html")

@app.route("/home")
def home():

    date_today = str(my_date.today())
    my_today = date_today
    
    def choose_gif(path):
    
        gif = random.choice(os.listdir(path))
    
        if gif[-4:] == "webp":
            return gif
        else:
            return choose_gif(path)
    
    image = choose_gif("/Users/michaelblack/Desktop/Michael Projects/flask/Soccer Scraping Flask/Soccer Flask/static")
    my_today = date_today
    
    return render_template("home_two.html", date_today=date_today, image=image)
  
@app.route("/fixtures", methods=["POST", "GET"])
def fixtures():
    
    if request.method == "POST":
        if request.form['submit_button'] == "View Matches":
            date = request.form.get("matchday")[:10]
            results = soccer_scraper.final_print(date)
            return results
        elif request.form['submit_button'] == "View/Refresh Today's Scores":
            date = str(my_date.today())
            results = soccer_scraper.final_print(date)
            return results
    else:
        date = str(my_date.today())
        results = soccer_scraper.final_print(date)
        
    return results

@app.route("/domestic_standings/<league_name>")
def standings(league_name):
    
    return soccer_standings.domestic(league_name)

@app.route("/cup_standings/<league_name>")
def standings_two(league_name):
    
    return cup_standings.cup(league_name)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)