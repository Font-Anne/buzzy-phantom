import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/main.html')
        html = main_template.render()
        self.response.write(html)

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/submit.html')
        html = main_template.render({
            'title' : self.request.get('title')
            'desc' : self.request.get('desc')
            'location' : self.request.get('location')
        })
        self.response.write(html)

class ViewHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/view.html')
        html = main_template.render({
            'title' : self.request.get('title')
            'desc' : self.request.get('desc')
            'location' : self.request.get('location')
        })
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/view', ViewHandler),
], debug=True)
