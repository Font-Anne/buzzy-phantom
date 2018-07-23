from google.appengine.ext import ndb

class Data(ndb.Model):
    title = ndb.StringProperty(required = True)
    desc = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
