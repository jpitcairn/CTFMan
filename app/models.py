from datetime import datetime
from app import db

class VirtualMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vm_id = db.Column(db.Integer, index=True)
    node = db.Column(db.String(120))
    name = db.Column(db.String(120), index=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<VirtualMachine {}>'.format(self.name)