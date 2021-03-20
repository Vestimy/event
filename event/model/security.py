# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------
from event import db
from sqlalchemy import String, Integer


class Confirmation(db.Model):
    __tablename__ = 'confirmation'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(128))
    conf_id = db.Column(String(128))


class Invite(db.Model):
    __tablename__ = 'invite'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(128))
    invite_id = db.Column(String(128))
    company_id = db.Column(Integer)
