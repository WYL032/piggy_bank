from flask import redirect, render_template, session
from flask import Flask, render_template, request
from models import db, User, CategorySection, Category, TransLog
from werkzeug.security import check_password_hash, generate_password_hash

import json
from enum import Enum

class Result:
    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def to_json(self):
        return json.dumps({
            'code': self.code,
            'data': self.data,
            'message': self.message
        })

class ResultCode(Enum):
    Success =1000
    InputError = 1010
    DataNotFound = 1020


@app.route("/login", methods=["POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return Result(ResultCode.InputError, None, "must provide username")
        elif not request.form.get("password"):
            return Result(ResultCode.InputError, None, "must provide password")
        user = db.session.query(User).filter_by(userName=request.form.get("username")).all()
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("password")):
             return Result(ResultCode.InputError, None, "must invalid username and/or password")
        session["user_id"] = user[0]["id"]
        return Result(ResultCode.Success, None, "login success")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        if password != request.form.get("confirmation"):
            return apology("password confirm fail", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0 :
            return apology("username already be used", 400)

        #for INSERT, the primary key of a newly inserted row (or None if none)
        userId = db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, generate_password_hash(password))
        session["user_id"] = userId
        return redirect("/")
    else:
        return render_template("register.html")
