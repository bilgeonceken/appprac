# appprac
###An i wanna learn flask project
A CRUD app. Unnecessarily tries to organize a university orienteering team

## Deploying to Heroku

```
heroku create
git push heroku master
heroku open
```

Alternatively, you can deploy your own copy of the app using this button:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

##How to set up locally  
You can use PostgreSQL or Sqlite as a database when setting up locally.  
Both situations are explained below.  
  
###Database chooice: Postgresql

+ Install PostgreSQL
+ After installation, create a new user to manage the database we'll be creating:
```
sudo adduser postgres_user
```

+ Enter "password" when it asks for password so you do not have to use your brain even just a little bit.

+ Log into the default PostgreSQL user (called "postgres") to create a database and assign it to the new user:
```
sudo su - postgres
psql
```

+ You will be dropped into the PostgreSQL command prompt.

+ Create a new user that matches the system user you created. Then create a database managed by that user:
```
CREATE USER postgres_user WITH PASSWORD 'password';
CREATE DATABASE my_postgres_db OWNER postgres_user;
```

+ Exit out of the interface with the following command:

```
\q
```

+ Exit out of the default "postgres" user account:
```
exit
```
database part is over

+ Clone, install reqs. and run app.py:

```
$ git clone https://github.com/kambafca/appprac  
$ cd appprac/
$ pip3 install -r requirements.txt
$ python3 app.py
```
+ then go to 127.0.0.1:5000 on your browser  
Default admin account:  
email   : kambafca@yopmail.com  
password: password

####Important: 
when you try something with models and database does not work, you might want to  
delete everything on the database and restart the app. to do that:

```
sudo su - postgres
psql
DROP DATABASE my_postgres_db;
CREATE DATABASE my_postgres_db OWNER postgres_user;
```

basically we delete and create the database again and again to reset it easily.    
  
Better write a migration script for everything else.

###Database chooice: Sqlite
```
$ git clone https://github.com/kambafca/appprac  
$ cd appprac/
$ pip3 install -r requirements.txt
```
+ on model.py, comment out line 28, uncomment line 29  
```
$ python3 app.py
```
+ then go to 127.0.0.1:5000 on your browser  
Default admin account:  
email   : kambafca@yopmail.com  
password: password  

#####todo stuff that comes into my mind

- [x] MAIN TODO: FIX THE POSTGRESQL DATABASE INTEGRATION PROBLEM WITH HEROKU  

- [x] Base structure
- [x] Theme and navigation structure
- [x] Twitter-like posting and stream(tutorial thingy)
- [x] Members page
- [x] Event model(trainings)
- [x] Github-like automatically generated unique(?) avatars
- [x] Flash messages(they already exists in view, just need to put them in templates)
- [x] Use avatar generator like password_hash_generator in model.py
- [x] Get rid of flask-bootstrap
- [ ] Find out why hashed passwords cause problem on PostgreSql and hash the passwords
- [ ] On active event, show "add" and "remove" buttons according to the users' situation and handle exceptions to avoid certain problems
- [ ] Learn how to unit test. lol
- [ ] Figure out how to store avatars on heroku to be able to reactivate avatar generator
- [ ] Fix competitors' order on "active event", first should be on top last on the bottom
- [ ] Profile pages
- [ ] User friendly create event and "register new user" pages
- [ ] "Add your name to week's events" pages
- [ ] Attandance records
- [ ] Automated e-mails
- [ ] Replace simplified user model with the real thing
- [ ] Public page for public
- [ ] ~~fix Momentjs, does not work properly~~
