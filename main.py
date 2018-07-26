import webapp2
import jinja2
import os
import information
import datetime
import time

from google.appengine.api import images
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/main.html')
        html = main_template.render()
        self.response.write(html)

#Sorts the post information in chonological order
        posts = information.Data.query()
        sorted_posts = posts.order(-information.Data.time).fetch()

#Writes out the HTML to create the post boxes
        for post in sorted_posts:
            self.response.write("<div class= 'box'>")
            self.response.write("<div class= 'post_info'>")
            self.response.write("<h2>" + post.title + "</h2>")
            self.response.write("<p></p><h3>" + post.desc + "</h3>")
            self.response.write("<p></p><p></p><h3>" + post.location + "</h3> </div>")
            if post.image:
                self.response.write("<p></p> <img class='picture' src='/img?id=" + str(post.key.id()) + "'>")
            self.response.write("</div>")
            self.response.write("<br></br>")

    def post(self):

        data = information.Data()
        data.title = self.request.get('title')
        data.desc = self.request.get('desc')
        data.location = self.request.get('location')
        data.time = datetime.datetime.now()
        if self.request.get("image"):
            data.image = images.resize(self.request.get("image"), 300, 300)
        data.put()
        time.sleep(1)

        main_template = jinja_env.get_template('templates/main.html')

        html = main_template.render({
            "title": data.title,
            "desc": data.desc,
            "location": data.location,
            "image": data.image
        })
        self.response.write(html)
        self.response.write("<p></p>")
        self.redirect("/")

#Sorts the post information in chonological order
#         posts = information.Data.query()
#         sorted_posts = posts.order(-information.Data.time).fetch()
#
# #Writes out the HTML to create the post boxes after the user clicks Submit button
#         for post in sorted_posts:
#             self.response.write("<div class= 'box'>")
#             self.response.write("<div id= 'post_image'>")
#             self.response.write("</div> <h2>" + post.title + "</h2>")
#             self.response.write("<p></p><h3>" + post.desc + "</h3>")
#             self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")
#             if post.image:
#                 self.response.write("<p></p> <img src='/img?id=" + str(post.key.id()) + "'>")
#             self.response.write("</div>")
#             self.response.write("<br></br>")

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render()
        self.response.write(html)

#Handler that deals with uploading images (No need to mess with this)
class Image(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("Data", int(self.request.get("id")))
        data = key.get()
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.write(data.image)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/about.html')
        html = main_template.render()
        self.response.write(html)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/img', Image),
    ('/about', WelcomeHandler)
], debug=True)
