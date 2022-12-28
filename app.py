# Importing functions from flask Library
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL

db = SQL("sqlite:///student.db")
d = SQL("sqlite:///sports.db")

# Creating a list of sports for which the students can registor for
'''Sports = [
    "Badminton",
    "Cricket",
    "Football",
    "Kabaddi",
    "Chess",
    "Volleyball"
]'''

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# creating the default route for the app
@app.route("/")
def index() :
    sports = d.execute("SELECT * FROM sport")
    return render_template("index.html",sports = sports )

@app.route("/signin", methods=["GET", "POST"])
def sign() :
    if not session.get("name") :
        if request.method == "GET" :
            return render_template("sign.html")
        name = request.form.get("name")
        email = request.form.get("email")
        if not name or not email :
            return render_template("sign.html")
        else :

            session["name"] = name 
            session["email"] = email
            login = db.execute("SELECT COUNT(*) FROM student WHERE email=?",email )
            if login[0]["COUNT(*)"] == 0 :
                db.execute("INSERT INTO student (name, email) VALUES(?, ?)", name, email )
            return redirect("/reg")
    return redirect("/reg")

@app.route("/reg")
def reg() :
   
    sports = d.execute("SELECT * FROM sport")
    return render_template("sport.html", sports=sports)

@app.route("/list", methods= ["GET", "POST"])
def list() :
    if "sport" not in session:
        session["sport"] = []

    if request.method == "POST" :
        id = request.form.get("id")
        if id:
            session["sport"].append(id)
            
        return redirect("/list")

    sports = d.execute("SELECT * FROM sport WHERE id IN (?)", session["sport"] )
    return render_template("list.html", sports = sports)
 
    
@app.route("/logout")
def logout() :
    session["name"] = None
    return redirect("/")    

