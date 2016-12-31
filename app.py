from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
from flask_bootstrap import Bootstrap
from flask_bcrypt import check_password_hash
import forms
import model
from peewee import *
from flask_moment import Moment
from flask_avatar import Avatar

app = Flask(__name__)
moment = Moment(app)

avatar=Avatar(app)
AVATAR_URL = "/static/avatars/<text>/<width>" #The avatar url,default '/avatar/<text>/<width>'
AVATAR_RANGE = [0,512] #set avatar range to allow generate,if disallow,abort(404).Default [0,512]

bootstrap=Bootstrap(app)

##Defined these here to make changes easily
DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app.secret_key = "asdfasdfasdf324134213423"

##SETTING UP LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


##this is a login manager instance method and
##instead of "login", we could define an absolute url as well
##If a not logged in user tries to access
## login required view we will redirect them to login view
##with this.
login_manager.login_view = "login"

##Documentation: You will need to provide a user_loader callback.
##This callback is used to reload the user object
## from the user ID stored in the session.
##It should take the unicode ID of a user,
##and return the corresponding user object.
@login_manager.user_loader
def load_user(user_id):
    """loads users"""
    try:
        ##.get() is not a dict. method but a peewee Model's instance method.
        ##getting the row where User.id equals user_id.
        ##peewee defines autoincerement primary_key id
        ## automatically even if you do not define it
        ## explicitly
        return model.User.get(model.User.id == user_id)
    ## If no row matches the .get() query
    ##peewee raises this error
    except model.DoesNotExist:
        return None

##For web-apps you will typically open a connection
##when a request is started and close it when the response is delivered:
@app.before_request
def before_request():
    """configures before request behavior"""
    g.db = model.DATABASE
    g.db.connect()
    ## current_user: flask_login object. returns current user
    ## BUT!!! current_user is just a proxy. never pass it as it is.
    ## user _get_current_object() instead
    g.user = current_user

##I must think about reasons to use g here.

##ABOUT the argument: request in after function:
##Documentation says that
##The return value of the view is then converted into an
## actual response object and handed over to the after_request()
## functions which have the chance to replace it or modify it in place.

##So maybe even if i dont give request argument to after_request function myself
##it takes it by default

##It does not take an argument, response in documentation
## however returning the defined response automatically
## makes sense
@app.after_request
def after_request(response):
    """configures after request behavior"""
    g.db.close()
    return response

@app.route("/register", methods=("GET", "POST"))
def register():
    """register view function"""
    ##we pass this to render template
    form = forms.RegisterForm()
    ##this method belongs to forms
    ##returns true when validators do not raise any error
    ##IMPORTANT:
    ##validate_on_submit will check if it is a POST request and if it is valid.
    ## So basically its like if method=POST in some manner
    if form.validate_on_submit():
        ##1st arg: flash message, 2nd arg: its category
        ##i dont know anything about flash messages right now, but still...
        flash("Successfully registered!", "success")

        ##pulls data from taken form and creates user accordingly
        ##do not forget that create_user() is a class method defined by us
        model.User.create_user(
            username=form.username.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            ##create_user func encrypts it
            password=form.password.data)
        ##its good to redirect after a post request
        return redirect(url_for("index"))
    ##if get request
    return render_template("register.html", form=form)

@app.route("/login", methods=("GET", "POST"))
def login():
    """login view function"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            ##compare emails first
            user = model.User.get(model.User.email == form.email.data)
        except model.DoesNotExist:
            flash("Wrong email or password", "error")
        else:
            ##and secondly passwords
            if check_password_hash(user.password, form.password.data):
                ##login_user() function creates sessions in users' browser, creates a cookie
                ##logout_user() deletes the session cookie created by login_user()
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash("Wrong email or password", "error")

    return render_template("login.html", form=form)

@app.route("/logout")
##you put this decorator to well... login required views.
@login_required
def logout():
    """logout view function"""
    logout_user()
    flash("Logged out!", "success")
    return redirect(url_for("index"))

@app.route("/post", methods=("GET", "POST"))
@app.route("/post/<int:page>", methods=("GET", "POST"))
@login_required
def post(page=1):
    """post view"""
    postsperpage=6
    allposts = model.Post.select().paginate(page,postsperpage)
    makspage = (allposts.count()/postsperpage) + 1
    form = forms.PostForm()
    if form.validate_on_submit():
        ##g.user=current_user and curret_user is just a proxy
        ## you must user _get_current_object() when passing it to
        ## places.
        model.Post.create(user = g.user._get_current_object(),
                          content=form.content.data.strip())
        flash("Post posted!")
        return redirect(url_for("post"))
    return render_template("post.html", form=form, allposts=allposts, page=page, makspage=makspage)

@app.route("/members")
@login_required
def members():
    teammembers = model.User.select()
    return render_template("members.html", teammembers=teammembers)

@app.route("/createevent", methods=("GET","POST"))
@login_required
def createevent():
    form = forms.EventForm()
    if form.validate_on_submit():
        model.Event.create_event(eventname=form.eventname.data, eventdatetime=form.eventdatetime.data,
                                 eventtype=int(form.eventtype.data), eventday=int(form.eventday.data))

        flash("Event created successfully")
        return redirect(url_for("nextevent"))
    return render_template("createevent.html", form=form)

@app.route("/nextevent")
@login_required
def nextevent():
    event = model.Event.select().get()
    return render_template("nextevent.html",event=event)

@app.route("/")
@login_required
def index():
    """index view"""
    return render_template("layout.html")

if __name__ == "__main__":
    model.initialize()
    try:
        ##Creates a superuser for us
        ##remember we defined this @classmethod ourselves on model.py
        model.User.create_user(
            username="kambafca",
            firstname="blg",
            lastname="onckn",
            email="kambafca@yopmail.com",
            password="password",
            admin=True)
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)
