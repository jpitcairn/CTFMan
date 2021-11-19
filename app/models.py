from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    virtual_machines = db.relationship('VirtualMachine', backref='creator', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class VirtualMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vm_id = db.Column(db.Integer, index=True)
    node = db.Column(db.String(120))
    name = db.Column(db.String(120), index=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<VirtualMachine {}>'.format(self.name)