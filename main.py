import webapp2
import jinja2
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from astrology_models import *
from google.appengine.api import users

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

#authuser checks if user is in datastore and if the password matches that user's
#should check for uniqueness of username & process password not as string
def userExists(email):
    if User.query().filter(User.email == email).get():
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
            createUser(nickname,email,"0")
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
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
            createUser(new_username,new_password,new_email)
            logout_url = users.create_logout_url('/profile?email={}'.format(new_email))
            self.redirect(logout_url)
class CatHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("cat.html")
        self.response.write(template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("profile.html")
        email = str(self.request.get('email'))
        print(userExists(email))
        user = users.get_current_user()
        print("EHEKHEHELHLIEUHB")
        print(type(email))
        print(User.query().filter(User.email == email).get())
        if userExists(email) :
            self.response.write(template.render({
                "username": User.query().filter(User.email == email).get().name
            }))
        elif user:
            createUser(
                user.nickname(),
                user.email(),
                "0"
            )
            self.response.write(template.render({
                "username": users.get_current_user().nickname()
            }))
        else:
            self.redirect('/login')

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
], debug=True)
