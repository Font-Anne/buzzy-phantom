from google.appengine.ext import ndb

class Data(ndb.Model):
    title = ndb.StringProperty(required = True)
    desc = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    image = ndb.BlobProperty(required = False)
    time = ndb.DateTimeProperty(required = True)
    tags = ndb.StringProperty(required = False, repeated = True)
