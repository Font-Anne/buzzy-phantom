import webapp2
import jinja2
import os
import information
import datetime

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

        all_posts = information.Data.query().fetch()
        for post in all_posts:
            self.response.write("<div class= 'box'>")
            self.response.write("<div id= 'post_image'>")
            self.response.write("</div> <h2>" + post.title + "</h2>")
            self.response.write("<p></p><h3>" + post.desc + "</h3>")
            self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")
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
            data.image = images.resize(self.request.get('image'), 300, 300)
        data.put()

        main_template = jinja_env.get_template('templates/main.html')
        all_posts = information.Data.query().fetch()

        html = main_template.render({
            "title": data.title,
            "desc": data.desc,
            "location": data.location,
            "image": data.image
        })
        self.response.write(html)
        self.response.write("<p></p>")
        for post in all_posts:
            self.response.write("<div class= 'box'>")
            self.response.write("<div id= 'post_image'>")
            self.response.write("</div> <h2>" + post.title + "</h2>")
            self.response.write("<p></p><h3>" + post.desc + "</h3>")
            self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")
            if post.image:
                self.response.write("<p></p> <img src='/img?id=" + str(post.key.id()) + "'>")
            self.response.write("</div>")
            self.response.write("<br></br>")

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render()
        self.response.write(html)

class Image(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("Data", int(self.request.get("id")))
        data = key.get()
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.write(data.image)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/img', Image)
], debug=True)
