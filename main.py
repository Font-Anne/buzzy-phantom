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

    def post(self):
        data = information.Data()
        data.title = self.request.get('title')
        data.desc = self.request.get('desc')
        data.location = self.request.get('location')
        data.image = images.resize(self.request.get('image'), 32, 32)
        data.put()

        main_template = jinja_env.get_template('templates/main.html')
        html = main_template.render({
            "title": data.title,
            "desc": data.desc,
            "location": data.location,
            "image": data.image
        })
        self.response.write(html)

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render()
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
], debug=True)
