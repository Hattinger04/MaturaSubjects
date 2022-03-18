from flask import Flask, session
from flask.templating import render_template
from flask import request, jsonify
from flask_restful import Resource, Api

import json
import string
import random
import hashlib
import keys

from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
api = Api(app)

app.secret_key = keys.secret_key
key = keys.requestkey
db = keys.db
subjects = keys.subjects

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(db)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
from dataclasses import dataclass

filename = "users.txt"

@dataclass
class User(Base):
    __tablename__ = 'User'

    ID = Column(Integer, primary_key=True)
    USERNAME = Column(Text, nullable=False)
    PASSWORD = Column(Text, nullable=False)
    SUBJECT1 = Column(Text)
    SUBJECT2 = Column(Text)


def checkExisting(username, password):
    return User.query.filter_by(USERNAME=username, PASSWORD=password).first()


def checkLogin(username, password):
    return User.query.filter_by(USERNAME=username, PASSWORD=password, SUBJECT1=None, SUBJECT2=None).first()


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def updateUser(username, password, subject1, subject2):
    user = User.query.filter_by(USERNAME=username, PASSWORD=password).first()
    user.SUBJECT1 = subject1
    user.SUBJECT2 = subject2
    db_session.add(user)
    db_session.flush()


@app.route('/')
def home():
    try:
        if session["login"]:
            return render_template("elections.html")
    except Exception:
        session["login"] = False
    return loginGetError("Not logged in")


@app.route('/login')
def loginGet():
    return render_template("login.html")


@app.route('/login')
def loginGetError(data):
    return render_template("login.html", data=data)

@app.route('/graphics')
def getGraphics():
    return render_template("graphics.html")


@app.route('/login', methods=["Post"])
def loginPost():
    session["user"] = checkLogin(request.form.get("username"), encrypt_string(request.form.get("password")))
    if session["user"] is not None:
        session["username"] = request.form.get("username")
        session["password"] = encrypt_string(request.form.get("password"))
        session["login"] = True;
        return render_template("elections.html")
    user = checkExisting(request.form.get("username"), encrypt_string(request.form.get("password")))
    if user:
        return getGraphics()
    return render_template("login.html", data="Wrong data")


@app.route('/subjectData', methods=["Post"])
def subjectData():
    taken_subjects = []
    for sub in subjects:
        if request.form.get(sub):
            taken_subjects.append(sub)
    updateUser(session["username"], session["password"], taken_subjects[0], taken_subjects[1])
    session.clear()
    return getGraphics()


class Data(Resource):
    def get(self):
        user = checkExisting(request.form["username"], (encrypt_string(request.form["password"])))
        if user:
            return jsonify({"message": user})
        return jsonify({"message": "no user found"})

    def put(self):
        print(request.form["users"])
        if request.form["key"] == key:
            for username in json.loads(request.form["users"]):
                password = get_random_string(10)
                with open(filename, "a") as f:
                    f.write("Username %s - Password %s \n" % (username, password))
                updateUser(USERNAME=username, PASSWORD=encrypt_string(password), SUBJECT1="", SUBJECT2="")
            return jsonify({"message": "all users successfully stored!"})
        return jsonify({"message": "you are not allowed to create new users!"})


api.add_resource(Data, '/data')

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, host="0.0.0.0")
