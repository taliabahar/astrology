from google.appengine.ext import ndb
from google.appengine.ext import blobstore

class Photo(ndb.Model):
    name = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    profilePicture = ndb.BlobKeyProperty()
