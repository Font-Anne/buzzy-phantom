import webapp2
import jinja2
import os
import information

### Need to make submit buttons a POST action

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/view.html')
        html = main_template.render()
        self.response.write(html)

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render()
        self.response.write(html)

class DataHandler(webapp2.RequestHandler):
    def get(self):
        data = information.Data()
        data.title = self.request.get('title')
        data.desc = self.request.get('desc')
        data.location = self.request.get('location')
        data.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/view', DataHandler)
], debug=True)
