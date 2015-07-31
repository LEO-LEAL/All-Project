#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
from google.appengine.api import users
import webapp2
import jinja2
import os
import logging
import urllib2
import json
import datetime

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/main'))
        self.response.write('<html><boby>%s</body></html>' % greeting)

class Comment(ndb.Model):
    user = ndb.StringProperty(required=True)
    message = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        query = Comment.query()
        comment_data = query.fetch()
        #login info
        user = users.get_current_user()
        greeting = ('Welcome, %s! (<a href=%s>sign_out</a>' %
            (user.nickname(), users.create_logout_url('/')))
        self.response.write('<html><boby>%s</body></html>' % greeting)
        #login end
        ## random gif
        url = "http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=cute+puppies"
        result = urllib2.urlopen(url)
        gif = json.loads(result.read())
        gif_url = gif['data']['image_url']
        ## enf of random gif
        template_vars = {'gif_url': gif_url, 'comments': comment_data}
        template = jinja2_environment.get_template('templates/index.html')
        self.response.write(template.render(template_vars))

class AddCommentHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        message = self.request.get('message')
        current_date = datetime.datetime.now()
        comment = Comment(user=user.nickname(), message=message)
        comment.created_date = current_date
        comment.put()
        template = jinja2_environment.get_template('templates/we_did_it.html')
        self.response.write(template.render())

class CommentViewHandler(webapp2.RequestHandler):
    def get(self):
        comment_id = self.request.get('comment_id')
        comment = Comment.get_by_id(int(comment_id))
        template_vars = {'comment': comment }
        template = jinja2_environment.get_template('templates/index.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/main', MainHandler),
    ('/addcomment', AddCommentHandler)
], debug=True)

jinja2_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
