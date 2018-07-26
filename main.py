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
        if self.request.get('tags'):
            sorted_posts = posts.filter(information.Data.tags == self.request.get('tags')).order(-information.Data.time).fetch()
        else:
            sorted_posts = posts.order(-information.Data.time).fetch()

#Writes out the HTML to create the post boxes
        for post in sorted_posts:
            if post.image:
                self.response.write("<div class= 'box'><table style='width: 100%'><tbody><tr><td>")
            else:
                self.response.write("<div class= 'box'>")
            if post.image:
                self.response.write("<img class='picture' src='/img?id=" + str(post.key.id()) + "'>")
                self.response.write("</td><td style='width: 50%;'>")
                self.response.write("<div class= 'image_info'>")
                self.response.write("<h2>" + post.title + "</h2>")
                self.response.write("<p></p><h3>" + post.desc + "</h3>")
                self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")

#Loops through a Data object's list of tags and writes them out in HTML
                if post.tags:
                    self.response.write("<div class= 'in_tags'>")
                    for tag in post.tags:
                        self.response.write("<a href='/?tags=%23" + tag[1:] + "'>" + tag + "</a> ")
                    self.response.write("<p></p>")
                self.response.write("</td></tr></tbody></table>")
                self.response.write("</div>")

            else:
                self.response.write("<div class= 'post_info'>")
                self.response.write("<h2>" + post.title + "</h2>")
                self.response.write("<p></p><h3>" + post.desc + "</h3>")
                self.response.write("<p></p><p></p><h3>" + post.location + "</h3>")

#Loops through a Data object's list of tags and writes them out in HTML
                if post.tags:
                    self.response.write("<div class= 'in_tags'>")
                    for tag in post.tags:
                        self.response.write("<a href='/?tags=%23" + tag[1:] + "'>" + tag + "</a> ")
                    self.response.write("<p></p>")
                self.response.write("</div>")


            self.response.write("</div>")
            self.response.write("</div>")
            self.response.write("<br></br>")

    def post(self):

        data = information.Data()
        data.title = self.request.get('title')
        data.desc = self.request.get('desc')
        data.location = self.request.get('location')
        data.time = datetime.datetime.now()

#Takes a singular String containing all #tags and puts them into a list.
#Each element in the list is inserted as a tag in the Datastore.
        tag_string = self.request.get('tags')
        tag_list = tag_string.split(" ")
        data.tags = tag_list


        if self.request.get("image"):
            data.image = images.resize(self.request.get("image"), 300, 300)
        data.put()
        time.sleep(1)

        main_template = jinja_env.get_template('templates/main.html')

        html = main_template.render({
            "title": data.title,
            "desc": data.desc,
            "location": data.location,
            "image": data.image,
            "tags": data.tags
        })
        self.response.write(html)
        self.response.write("<p></p>")
        self.redirect("/")

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
