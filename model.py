import datetime
from peewee import (CharField, Model, SqliteDatabase, DateTimeField,
                    BooleanField, TextField,
                    ForeignKeyField, IntegrityError, DoesNotExist)
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash


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
    def create_user(cls, username, email, password, admin=False):
        """creates a new user"""
        try:
            cls.create(username=username, email=email,
                       password=generate_password_hash(password),
                       is_admin=admin)
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
        database=DATABASE
        ##newest items first
        order_by = ("-timestamp",)

##we call this function on app.py
##to create the tables if not exists
def initialize():
    """Initilizes the database"""
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
