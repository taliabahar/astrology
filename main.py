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
def authUser(username, password):
    existing_users = User.query().filter(User.name == username).fetch()
    for person in existing_users:
        if person.password == password:
            return True
        else:
            return False
#will create a user based on given parameters
#should edit to take a user object containing every parameter
def createUser(username,password,email):
    user = User(
        name = username,
        password = password,
        email = email
    )
    user.put()

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("index.html")
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
            print(greeting)
        else:
            self.redirect('/login')
        self.response.write(template.render());

#incorporate google login_url to use google account
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("login.html")
        login_url = users.create_login_url('/')
        self.response.write(template.render({
            "login_url": login_url
        }))
    def post(self):
        user = users.get_current_user()
        name = self.request.get('username')
        password = self.request.get('password')
        new_username = self.request.get('username-new')
        new_password = self.request.get('password-new')
        email = self.request.get('email');
        if authUser(name,password):
            self.redirect('/profile')
        else:
            createUser(new_username,new_password,email)
            self.redirect('/profile')

class CatHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("cat.html")
        self.response.write(template.render())

# class RecipeDisplayHandler(webapp2.RequestHandler):
#     def post(self):
#         query = self.request.get('query')
#         base_url = 'http://www.recipepuppy.com/api/?'
#         params = { 'q': query }
#         response = urlfetch.fetch(base_url + urlencode(params)).content
#         results = json.loads(response)
#
#         template = jinja_env.get_template('templates/recipe.html')
#         self.response.write(template.render({
#             'results': results
#         }))

class HoroscopeHandler(webapp2.RequestHandler):
    def get(self):
        # query = self.request.get('query')
        base_url = 'https://aztro.sameerkumar.website/?'
        params = {'sign' : 'leo', 'day' : 'today'} #need to set sign to users sign
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


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("profile.html")
        user = users.get_current_user()
        if user:
            self.response.write(template.render({
                "username": user.nickname()
            }))
        else:
            self.redirect('/login')
# class LoginHandler(webapp2.RequestHandler):
#     def get(self):
#         new_user_template = jinja_env.get_template("templates/login.html")
#         google_login_template = jinja_env.get_template("templates/google_login.html")
#         # get Google user
#         user = users.get_current_user()
#
#         if user:
#             # look for user in datastore
#             existing_user = User.query().filter(User.email == user.email()).get()
#             nickname = user.nickname()
#             if not existing_user:
#                 fields = {
#                   "nickname": nickname,
#                   "logout_url": logout_url,d
#                 }
#                 # prompt new users to sign up
#                 self.response.write(new_user_template.render(fields))
#             else:
#                 # direct existing user to feed
#                 self.redirect('/profile')
#                 return
#         else:
#             # Ask user to sign in to Google
#             self.response.write(google_login_template.render({ "login_url": login_url }))
#
#
# class Profile(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_env.get_template('/templates/profile.html')
#         user = users.get_current_user()
#         current_user = User.query().filter(User.email == user.email()).get()
#         profile_fields = create_profile(current_user)
#         self.response.write(template.render(profile_fields))
#
#     def post(self):
#         user = users.get_current_user()
#         if not user:
#             self.redirect('/')
#             return
#         current_user = User.query().filter(User.email == user.email()).get()
#         if not current_user:
#             # upon new user form submission, create new user and store in datastore
#             new_user_entry = User(
#             user_name = self.request.get("name"),
#             user_nickname = self.request.get("username"),
#             email = user.email(),
#             )
#             new_user_entry.put()
#             current_user = new_user_entry
#         time.sleep(.2)
#         self.redirect('/profile')
#         return
#
#
# class GenreChooser(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_env.get_template('/templates/genre_chooser.html')
#         self.response.write(template.render())
#
# class DifficultyChooser(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_env.get_template('/templates/difficulty_chooser.html')
#         self.response.write(template.render())
#
# class GameHandler(webapp2.RequestHandler):
#     def get(self):
#         genre = self.request.get("genre")
#         random_function = random_song(genre)
#         template=jinja_env.get_template('/templates/game.html')
#         self.response.write(template.render(random_function))
#
# class RandomQuestionHandler(webapp2.RequestHandler):
#     def get(self):
#         genre = self.request.get("genre")
#         self.response.headers['Content-Type'] = 'application/json'
#         random_function = random_song(genre)
#         self.response.out.write(json.dumps(random_function))
#
#
# class EndgameHandler(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_env.get_template('/templates/end_game.html')
#         user = users.get_current_user()
#         current_user = User.query().filter(User.email == user.email()).get()
#         profile_fields = create_profile(current_user)
#         self.response.write(template.render(profile_fields))
#
# class SeedHandler(webapp2.RequestHandler):
#     def get(self):
#         seed_data()
#         self.response.write('Data Loaded')
#
# class UpdateScoreHandler(webapp2.RequestHandler):
#     def get(self):
#         new_score = int(self.request.get("new"))
#         user = users.get_current_user()
#         current_user = User.query().filter(User.email == user.email()).get()
#         current_user.score = new_score
#         current_user.put()
#         if new_score > current_user.highscore:
#             current_user.highscore = new_score
#             current_user.put()
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

class CatHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("photoForm.html")
        var = {}
        var['upload_url']= blobstore.create_upload_url('/upload_photo')
        self.response.write(template.render(var))



app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LoginHandler),
    ('/profile', ProfileHandler),
    ('/cat', CatHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/photoForm', FormHandler),
    ('/picture/([^/]+)?', MediaHandler),
    ('/horoscope', HoroscopeHandler)
], debug=True)
