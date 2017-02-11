import datetime
from peewee import (CharField, IntegerField, DateTimeField, BooleanField,
                    SqliteDatabase, Model, IntegrityError, ForeignKeyField,
                    TextField, DoesNotExist, Proxy, PostgresqlDatabase,
                   )
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
##from avatarcreator import createavatar
import os

# Import modules based on the environment.
# The HEROKU value first needs to be set on Heroku
# either through the web front-end or through the command
# line (if you have Heroku Toolbelt installed, type the following:
# heroku config:set HEROKU=1).
# On this repo though, app.json tells heroku to create an env. variable
# "HEROKU"="1" so no need to do anything.

# For even more control over how your database is defined/initialized,
# we use the Proxy helper.
# Proxy objects act as a placeholder,
# and then at run-time you can swap it out for a different object.
db_proxy = Proxy()

# Different init options for heroku and local.
# As mentioned above, we need "HEROKU" env variable in heroku
if "HEROKU" in os.environ:
    import urllib.parse as ur
    import psycopg2
    ur.uses_netloc.append("postgres")
    url = ur.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    db_proxy.initialize(db)
else:
    db = PostgresqlDatabase('my_postgres_db', user='postgres_user', password='password', host='localhost')
    # db = SqliteDatabase("userdatabase.db")
    db_proxy.initialize(db)

## User mixin provides some useful stuff
class User(UserMixin, Model):
    """User model object"""
    ##peewee automatically adds autoinc. id column.
    username = CharField(unique=True)
    password = CharField(max_length=50)
    email = CharField(unique=True)
    ## todo: answer why timestampfield but not datetimefield?
    ##also notice it is not now(), but just now
    ##joined_at=TimestampField(default=datetime.datetime.now)
    joined_at = DateTimeField(default=datetime.datetime.now)
    firstname = CharField()
    lastname = CharField()
    ####ex: birthday=date(1960, 1, 15)
    ##birthday = DateField()
    avatarloc = CharField(default="/static/avatars/default.png")
    is_admin = BooleanField(default=False)

    class Meta:
        """defines database related to model and stuff"""
        database = db_proxy
        ##its a tuple. so put  , at the end.
        ##you will not understand the error if you forget that.
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, firstname, lastname, email, password, admin=False):
        """creates a new user"""
        try:
            cls.create(username=username, firstname=firstname,
                       lastname=lastname, email=email,
                       #password=generate_password_hash(password),
                       password=password,
                       is_admin=admin
                       ## createavatar funtion takes username as argument
                       ## and generates and avatar accordingly. Returns location
                       ## of the avatar to be added to the database
                       ##,avatarloc=createavatar(username)
                      )
        except IntegrityError:
            raise ValueError("User already exists")

    ##Typically a for. key will contain primary key of the model
    ##it relates to. but you can specify a "to_field."
    ##check documentation
class Post(Model):
    """Post model object"""
    timestamp = DateTimeField(default=datetime.datetime.now)
    ##related_name = "posts" means now these is some_user.posts
    user = ForeignKeyField(
        rel_model=User,
        related_name="posts",
        )
    content = TextField()
    class Meta:
        """defines database the model related to and stuff"""
        database = db_proxy
        ##newest items first
        order_by = ("-timestamp",)

class Event(Model):
    """ Training event model """
    eventname = CharField()
    eventdatetime = DateTimeField()
    eventcontent = CharField()
    ## 0: orienteering, 1: running
    eventtype = IntegerField()
    ##0:monday, 1:tuesday 2: wednesday, ,4: thursday 5: saturday, 6: sunday
    eventday = CharField()
    class Meta:
        database = db_proxy
        order_by = ("-eventdatetime",)

    @classmethod
    def create_event(cls, eventname, eventdatetime, eventtype, eventday, eventcontent):
        """creates a new event"""
        try:
            cls.create(eventname=eventname, eventdatetime=eventdatetime,
                       eventtype=eventtype, eventday=eventday,
                       eventcontent=eventcontent
                      )
        except IntegrityError:
            raise ValueError("Event already exists")


class UserEvent(Model):
    competitor = ForeignKeyField(User, related_name="competitors")
    event = ForeignKeyField(Event, related_name="events")
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db_proxy
        order_by = ("-timestamp",)

##we call this function on app.py
##to create the tables if not exists
def initialize():
    """Initilizes the database"""
    db_proxy.connect()
    ## it does not matter from peewee's perspective which model
    ##the manytomany field goes on
    ##since the back-reference is just the mirror image.
    ## In order to write valid Python, though, you will need to add the
    ## ManyToManyField on the second model so that the name of the first model is in the scope.
    ## We still need a junction table to store the relationships between students and courses.
    ## This model can be accessed by calling the get_through_model() method.
    ## This is useful when creating tables.
    db_proxy.create_tables([User, Post, Event, UserEvent], safe=True)
    db_proxy.close()
