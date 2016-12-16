from flask import Flask,g,render_template,flash,redirect,url_for
from flask_login import LoginManager, login_user,logout_user,login_required
from flask_bcrypt import check_password_hash
##FlaskWTFDeprecationWarning: "flask_wtf.Form" has been renamed to "FlaskForm" and will
##be removed in 1.0.
import forms
import model

app=Flask(__name__)


##Defined these here to make changes easily
DEBUG=True
PORT=8000
HOST="0.0.0.0"

app.secret_key="asdfasdfasdf324134213423"

##SETTING UP LOGIN MANAGER
login_manager=LoginManager()
login_manager.init_app(app)


##this is a login manager instance method and
##instead of "login", we could define an ansolute url as well
##If a not logged in user tries to access
## login required view we will redirect them to login view
##with this.
login_manager.login_view="login"


##Documentation: You will need to provide a user_loader callback.
##This callback is used to reload the user object
## from the user ID stored in the session.
##It should take the unicode ID of a user,
##and return the corresponding user object.
@login_manager.user_loader
def load_user(user_id):
    try:
        return model.User.get(model.User.id==user_id)
    ## A peewee error
    except model.DoesNotExist:
        return None


##For web-apps you will typically open a connection
##when a request is started and close it when the response is delivered:
@app.before_request
def before_request():
    g.db=model.DATABASE
    g.db.connect()

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
    g.db.close()
    return response

##TODO:Read teardown request part: http://flask.pocoo.org/docs/0.11/reqcontext/


@app.route("/register", methods=("GET","POST"))
def register():
    ##we pass this to render template
    form=forms.RegisterForm()
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
            email=form.email.data,
            ##create_user func encrypts it
            password=form.password.data,
        )
        ##its good to redirect after a post request
        return redirect(url_for("index"))
    ##if get request
    return render_template("register.html",form=form)

@app.route("/login",methods=("GET","POST"))
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            ##compare emails first
            user=model.User.get(model.User.email==form.email.data)
        except model.DoesNotExist:
            flash("Wrong email or password", "error")
            print("Olmadi")
        else:
            print("Try gecti")
            ##and secondly passwords
            if check_password_hash(user.password, form.password.data):
                ##login_user() function creates sessions in users' browser, creates a cookie
                ##logout_user() deletes the session cookie created by login_user()
                login_user(user)
                print("login ettim")
                flash("Logged in successfully!","success")
                return redirect(url_for("index"))
            else:
                flash("Wrong email or password", "error")

    return render_template("login.html",form=form)

@app.route("/logout")
##you put this decorator to well... login required views.
@login_required
def logout():
    logout_user()
    flash("Logged out!","success")
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("layout.html")

if __name__=="__main__":
    model.initialize()
    try:
        ##Creates a superuser for us
        ##remember we defined this @classmethod ourselves on model.py
        model.User.create_user(
            username="kambafca",
            email="kambafca@mynet.com",
            password="password",
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG,port=PORT,host=HOST)
