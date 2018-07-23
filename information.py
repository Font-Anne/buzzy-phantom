from google.appengine.ext import ndb

class Data(ndb.Model):
    type = ndb.StringProperty(required = True)
    size = ndb.IntegerProperty(required = True)
    color = ndb.StringProperty(required = False)
    brand = ndb.StringProperty(required = True)
