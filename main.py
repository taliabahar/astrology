import webapp2
import jinja2
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from astrology_models import *
from google.appengine.api import users
import json
import os
from urllib import urlencode
from google.appengine.api import urlfetch
import urllib
from pprint import pprint
from pprint import pformat
import logging

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

#authuser checks if user is in datastore and if the password matches that user's
#should check for uniqueness of username & process password not as string
def userExists(email):
    if User.query().filter(User.email == str(email)).get():
        print(True)
        return True
    else:
        print(False)
        return False

def userInStore(email, password):
    existing_users = User.query().filter(User.email == email).fetch()
    for person in existing_users:
        if person.password == password:
            return True
        else:
            return False
#will create a user based on given parameters
#should edit to take a user object containing every parameter
def createUser(username,password,email):
    if userInStore(email,password):
        return False
    else:
        user = User(
            name = username,
            password = password,
            email = email
        )
        user.put()
        return True

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("index.html")
        google_user = users.get_current_user()
        if google_user:
            nickname = google_user.nickname()
            email = google_user.email()
            createUser(nickname,"0",email)
            logout_url = users.create_logout_url('/login')
            greeting = 'Welcome, {}! <a href="{}">sign out</a>'.format(
                nickname, logout_url)
            self.response.write(template.render({
                'greeting':greeting
            }));
        else:
            greeting = 'Welcome User!'
            self.response.write(template.render({
                'greeting':greeting
            }));


#incorporate google login_url to use google account
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("login.html")
        login_url = users.create_login_url('/profile')
        greeting = '<a href="{}">google sign in</a>'.format(
            login_url)
        self.response.write(template.render({
            "greeting": greeting
        }))
    def post(self):
        name = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')
        new_username = self.request.get('username-new')
        new_password = self.request.get('password-new')
        new_email = self.request.get('email-new');
        if userInStore(email,password):
            logout_url = users.create_logout_url('/profile?email={}'.format(email))
            self.redirect(logout_url)
        else:
            createUser(new_username,new_password,str(new_email))
            logout_url = users.create_logout_url('/profile?email={}'.format(new_email))
            self.redirect(logout_url)

class CatHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("cat.html")
        self.response.write(template.render())

class SignHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("pickSign.html")
        self.response.write(template.render())
    def post(self):
        sign = self.request.get("signs")
        user = users.get_current_user()
        if user:
            user_model=User.query().filter(User.email == user.email()).get()
            user_model.sign = sign
            user_model.put()
        self.redirect('/profile')

class HoroscopeHandler(webapp2.RequestHandler):
    def get(self):
        # query = self.request.get('query')
        user = users.get_current_user()
        if user:
            sign=User.query().filter(User.email == user.email()).get().sign

            base_url = 'https://aztro.sameerkumar.website/?'
            params = {'sign' : sign, 'day' : 'today'} #need to set sign to users sign
            #params = {'sign' : self.request.get('sign'), 'day' : 'today'}
            payload = urllib.urlencode(params)
            myurl = base_url + urlencode(params)
            # logging.info("URL: " + myurl)
            response = urlfetch.fetch(base_url + urlencode(params), method=urlfetch.POST, payload=payload).content
            results = json.loads(response)
            logging.info(pformat(results))

            template = jinja_env.get_template('horoscope.html')
            self.response.write(template.render({
                'results': results
            }))
        else:
            self.redirect('/login')
class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("profile.html")
        email = str(self.request.get('email'))
        user = users.get_current_user()
        # print("EHEKHEHELHLIEUHB")
        # print(type(email))
        # print(User.query().filter(User.email == email).get())
        if userExists(email) :
            self.response.write(template.render({
                "username": User.query().filter(User.email == email).get().name,
                "upload_url": blobstore.create_upload_url('/pic'),
            }))
        elif user:
            createUser(
                user.nickname(),
                "0",
                user.email(),
            )
            object = User.query().filter(User.email == user.email()).get()
            image = object.profilePicture
            sign = object.sign
            #print(User.query().filter(User.email == user.email()).get().profilePicture)
            # image = User.query().filter(User.email == user.email()).get().profilePicture
            # print(userExists(email))

            self.response.write(template.render({
                "username": users.get_current_user().nickname(),
                "upload_url": blobstore.create_upload_url('/pic'),
                "image": image,
                "sign": sign
            }))
        else:
            self.redirect('/login')
class ProfilePicHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        google_user = users.get_current_user();
        upload = self.get_uploads()[0]
        photo = Photo(
            blob_key = upload.key(),
        )
        photo.put()
        print("[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]")
        print(User.query().filter(User.email==google_user.email()))
        stored_user = User.query().filter(User.email == google_user.email()).get()
        stored_user.profilePicture = photo.blob_key;
        stored_user.put()
        self.redirect('/profile')

class FormHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("photoForm.html")
        var = {}
        var['upload_url']= blobstore.create_upload_url('/upload_photo')
        self.response.write(template.render(var))
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
        def post(self):
            name = self.request.get('name')
            upload = self.get_uploads()[0]
            photo = Photo(
                blob_key = upload.key(),
                name = name,
            )
            photo.put()
            self.redirect('/picture/{}'.format(upload.key()))

class MediaHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)



app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LoginHandler),
    ('/profile', ProfileHandler),
    ('/cat', CatHandler),
    ('/sign', SignHandler),
    ('/horoscope', HoroscopeHandler),
    ('/pic', ProfilePicHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/photoForm', FormHandler),
    ('/picture/([^/]+)?', MediaHandler),
], debug=True)
