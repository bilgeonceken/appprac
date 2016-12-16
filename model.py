import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash


DATABASE=SqliteDatabase("userdatabase.db")

##i do not know what user mixin does
## but is it recommened
class User(UserMixin, Model):
    username=CharField(unique=True)
    password=CharField(max_length=12)
    email=CharField(unique=True)
    ##TODO: answer why timestampfield but not datetimefield?
    ##also notice it is not now(), but just now
    ##joined_at=TimestampField(default=datetime.datetime.now)
    joined_at=DateTimeField(default=datetime.datetime.now)

    is_admin=BooleanField(default=False)

    class Meta:
        database=DATABASE
        ##its a tuple. so , at the end.
        ##you will not understand the error if you forget that.
        ##order_by=('-joined_at',)

    @classmethod
    def create_user(cls,username,email,password,admin=False):
        try:
            cls.create(username=username,email=email,password=generate_password_hash(password),is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

##we call this function on app.py
##to create the tables if not exists
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User],safe=True)
    DATABASE.close()

