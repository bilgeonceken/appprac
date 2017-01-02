import datetime
import subprocess
from peewee import (CharField, IntegerField, DateTimeField, BooleanField,
                    SqliteDatabase, Model, IntegrityError, ForeignKeyField,
                    TextField, DoesNotExist)
from playhouse.fields import ManyToManyField
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
## we call a python2 script to generate
## user avatars for us
from avatarClass import Avatar
DATABASE = SqliteDatabase("userdatabase.db")

##i do not know what user mixin does
## but is it recommened
class User(UserMixin, Model):
    """User model object"""
    ##peewee automatically adds autoinc. id column.
    username = CharField(unique=True)
    password = CharField(max_length=12)
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
        database = DATABASE
        ##its a tuple. so put  , at the end.
        ##you will not understand the error if you forget that.
        order_by = ('-joined_at',)

    def get_posts(self):
        """gets posts"""
        return Post.select().where(Post.user == self)

    def get_stream(self):
        """gets post stream"""
        return Post.select().where(
            (Post.user == self)
        )

    @classmethod
    def create_user(cls, username, firstname, lastname, email, password, admin=False):
        """creates a new user"""
        try:
            cls.create(username=username, firstname=firstname,
                       lastname=lastname, email=email,
                       password=generate_password_hash(password),
                       is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")
        ## if creation is succesful, than we create a random avatar for them
        else:
            ## default directory: ./static/avatars/<username>
            ## drops a username.png in that folder
            subprocess.Popen(["mkdir", "./static/avatars/"+username])
            subprocess.Popen(["python2", "avatarcreatorFORPY-2.7.py", username])

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
        database = DATABASE
        ##newest items first
        order_by = ("-timestamp",)


# DateField has properties for:
#
#     year
#     month
#     day
#
# TimeField has properties for:
#
#     hour
#     minute
#     second
#
# DateTimeField has all of them

class Event(Model):
    """ Training event model """
    eventname = CharField()
    eventdatetime = DateTimeField()
    competitors = ManyToManyField(User, related_name="events")
    eventcontent = CharField()
    ## 0: orienteering, 1: running
    eventtype = IntegerField()
    ##0:monday, 1:tuesday 2: wednesday, ,4: thursday 5: saturday, 6: sunday
    eventday = CharField()
    class Meta:
        database = DATABASE
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

##we call this function on app.py
##to create the tables if not exists
def initialize():
    """Initilizes the database"""
    DATABASE.connect()
    ## it does not matter from peewee's perspective which model
    ##the manytomany field goes on
    ##since the back-reference is just the mirror image.
    ## In order to write valid Python, though, you will need to add the
    ## ManyToManyField on the second model so that the name of the first model is in the scope.
    ## We still need a junction table to store the relationships between students and courses.
    ## This model can be accessed by calling the get_through_model() method.
    ## This is useful when creating tables.
    DATABASE.create_tables([User, Post, Event, Event.competitors.get_through_model()], safe=True)
    DATABASE.close()


### MANY TO MANY TUTORIAL
#
# from peewee import *
# from playhouse.fields import ManyToManyField
#
# db = SqliteDatabase('school.db')
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
# class Student(BaseModel):
#     name = CharField()
#
# class Course(BaseModel):
#     name = CharField()
#     students = ManyToManyField(Student, related_name='courses')
#
# StudentCourse = Course.students.get_through_model()
#
# db.create_tables([
#     Student,
#     Course,
#     StudentCourse])
#
# # Get all classes that "huey" is enrolled in:
# huey = Student.get(Student.name == 'Huey')
# for course in huey.courses.order_by(Course.name):
#     print course.name
#
# # Get all students in "English 101":
# engl_101 = Course.get(Course.name == 'English 101')
# for student in engl_101.students:
#     print student.name
#
# # When adding objects to a many-to-many relationship, we can pass
# # in either a single model instance, a list of models, or even a
# # query of models:
# huey.courses.add(Course.select().where(Course.name.contains('English')))
#
# engl_101.students.add(Student.get(Student.name == 'Mickey'))
# engl_101.students.add([
#     Student.get(Student.name == 'Charlie'),
#     Student.get(Student.name == 'Zaizee')])
#
# # The same rules apply for removing items from a many-to-many:
# huey.courses.remove(Course.select().where(Course.name.startswith('CS')))
#
# engl_101.students.remove(huey)
#
# # Calling .clear() will remove all associated objects:
# cs_150.students.clear()
