from flask import Flask, render_template, request
import sqlite3, datetime, os

app = Flask(__name__)

def detect_file(filename):
    if "virus" in filename.lower():
        return "Malicious"
    return "Safe"

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/scan", methods=["GET","POST"])
def scan():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        filename = file.filename
        result = detect_file(filename)

        conn = sqlite3.connect("scans.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS scans (file TEXT, result TEXT, time TEXT)")
        c.execute("INSERT INTO scans VALUES (?,?,?)",
                  (filename, result, str(datetime.datetime.now())))
        conn.commit()
        conn.close()

    return render_template("scan.html", result=result)

@app.route("/history")
def history():
    conn = sqlite3.connect("scans.db")
    c = conn.cursor()
    scans = c.execute("SELECT * FROM scans").fetchall()
    conn.close()
    return render_template("history.html", scans=scans)

@app.route("/about")
def about():
    return render_template("about.html")

app.run(debug=True)
