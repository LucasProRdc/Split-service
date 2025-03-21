from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class ControlSftp(db.Model):
    __table_name__ = 'control_sftp'

    country = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)

    def __init__(self, country, date, message, file_name):
        self.country = country
        self.date = date
        self.message = message
        self.file_name = file_name
