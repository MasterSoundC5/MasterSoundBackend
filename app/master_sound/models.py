from datetime import datetime

from app.db import db, BaseModelMixin


class Country(db.Model, BaseModelMixin):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True)
    iso = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    spanish_name = db.Column(db.String(45), nullable=False)
    users = db.relationship('User', back_populates='country', cascade='all, delete, delete-orphan', passive_deletes=True)


class User(db.Model, BaseModelMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.country_id', ondelete='CASCADE'), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, nullable=False, default=1)
    country = db.relationship('Country', back_populates='users')

