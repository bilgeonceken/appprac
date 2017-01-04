# appprac
###An i wanna learn flask project
####Unnecessarily tries to organize a university orienteering team

if you are planning to use sqlite(which you should if you just want to take a look at the app)  
just follow "how to set up locally steps", in this read me.  
If you want to use postgresql however, follow these steps:

###How to set up locally(for Postgresql)
+ install postgresql
+ After installation, create a new user to manage the database we'll be creating:
```
sudo adduser postgres_user
```
+ enter password when it asks its password

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
+ then start app.py and go to 127.0.0.1:5000 on your browser.  
admin account:  
kambafca@yopmail.com  
password  
  
+ These steps are enough to get it working but i'll copy paste rest of the tutorial anyway.  

+ Exit out of the interface with the following command:
```
\q
```
+ Exit out of the default "postgres" user account and log into the user you created with the following commands:
```
exit
sudo su - postgres_user
```
+ Sign into the database you created with the following command:
```
psql my_postgres_db
```
+ most importantly when you try something and broke the database, you might want to  
delete everything on the database and restart the app. to do that:

stop app.py and then
```
sudo su - postgres
psql
DROP DATABASE my_postgres_db;
CREATE DATABASE my_postgres_db OWNER postgres_user;
```
basically we create the database again and again this way to reset everything.  
probably i would not want to do that if actually brake an actually used, full of data, database.


##how to set up locally(for sqlite):
```
$ git clone https://github.com/kambafca/appprac  
$ cd appprac/
$ pip3 install -r requirements.txt
```
+ on model.py comment out line 28, uncomment line 29  
```
$ python3 app.py
```
+ then go to 127.0.0.1:5000 on your browser  
Default admin account:  
email   : kambafca@yopmail.com  
password: password  


note to myself: clean up non-url_for links if problems occur when actually hosting the thing  

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
- [ ] Profile pages
- [ ] User friendly create event and "register new user" pages
- [ ] "Add your name to week's events" pages
- [ ] Attandance records
- [ ] Automated e-mails
- [ ] Replace simplified user model with the real thing
- [ ] Public page for public
- [ ] fix Momentjs, does not work properly
