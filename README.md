# appprac
###An i wanna learn flask project
####Unnecessarily tries to organize a university orienteering team

how to set up locally:
```
$ git clone https://github.com/kambafca/appprac  
$ cd appprac/  
$ pip3 install -r requirements.txt
$ python3 app.py
```
then go to 127.0.0.1:8000 on your browser  
Default admin account:  
email   : kambafca@yopmail.com  
password: password  


note to myself: clean up non-url_for links if problems occur when actually hosting the thing  

#####todo stuff that comes into my mind
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
