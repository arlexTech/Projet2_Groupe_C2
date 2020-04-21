import sqlite3

from flask import Flask, render_template,flash, jsonify, g,request
from random import sample

app = Flask(__name__) #création d'une app flask

dbp = "inginious.sqlite" #chemin vers la db

def dic(cursor, row):
    return dict((cursor.description[i][0], value)
    for i, value in enumerate(row))

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(dbp)
    db.row_factory = dic
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def query_db(query, args=(), u=False):
    c = get_db().execute(query, args)
    sd = c.fetchall()
    c.close()
    return (sd[0] if sd else None) if u else sd


with app.app_context():
    c = get_db().cursor()

@app.route("/")
def index3():
    return render_template("chart.html")

@app.route("/g1")
def avgtries():
    return jsonify({"avgtries": query_db("select avg(tried) as val, task as lbl from user_tasks group by task")})

@app.route("/g23")
def results():
    return jsonify({"results": query_db("SELECT count(result) as val,course as lbl from submissions WHERE result='failed' GROUP BY course")})



if __name__ == "__main__":
    app.run(debug=True)