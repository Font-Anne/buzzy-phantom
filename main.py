import webapp2
import jinja2
import os
import information
from google.appengine.api import images

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
            self.response.write("</div>")
            self.response.write("<br></br>")

    def post(self):
        data = information.Data()
        data.title = self.request.get('title')
        data.desc = self.request.get('desc')
        data.location = self.request.get('location')
        # data.image = images.resize(self.request.get('image'), 32, 32)
        data.put()

        main_template = jinja_env.get_template('templates/main.html')
        all_posts = information.Data.query().fetch()

        html = main_template.render()
        self.response.write(html)

        self.response.write("<div class= 'box'>")
        self.response.write("<div id= 'post_image'>")
        self.response.write("</div> <h2>" + data.title + "</h2>")
        self.response.write("<p></p><h3>" + data.desc + "</h3>")
        self.response.write("<p></p><p></p><h3>" + data.location + "</h3>")
        self.response.write("</div>")
        self.response.write("<br></br>")

        for post in all_posts:
            self.response.write("<div class= 'box'>")
            self.response.write("<div id= 'post_image'>")
            self.response.write("</div> <h2>" + post.title + "</h2>")
            self.response.write("<p></p><h3>" + post.desc + "</h3>")
            self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")
            self.response.write("</div>")
            self.response.write("<br></br>")

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render()
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
], debug=True)
