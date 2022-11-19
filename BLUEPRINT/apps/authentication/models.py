# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from flask import session
from apps.home.models import AppointMent


from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    appointment = db.relationship('AppointMent', backref='patient', lazy=True)



    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Doctors(db.Model, UserMixin):
    __tablename__ = 'Doctors'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    Hospital = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(64), unique=True)
    appointment = db.relationship('AppointMent', backref='doctor', lazy=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.Hospital)

class pics (db.Model):
    __tablename__ = 'pics'
    picsid=db.Column(db.Integer,primary_key=True)
    id = db.Column(db.Integer,foreign_key=True)
    pic1=db.Column(db.String(100))
    pic2=db.Column(db.String(100))
    pic3=db.Column(db.String(100))

class scores (db.Model):
    __tablename__ = 'scores'
    scoreid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, foreign_key=True)
    score1= db.Column(db.Integer)
    score2= db.Column(db.Integer)







@login_manager.user_loader
def user_loader(id):
    if 'user_type' in session:
        if session["user_type"] == "patient":
            print("patient")
            return Users.query.filter_by(id=id).first()
        if session["user_type"] == "doctor":
            print("doctor")
            return Doctors.query.filter_by(id=id).first()



@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None




