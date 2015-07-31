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
import datetime
import webapp2
import jinja2
import os
import logging

class Comment(ndb.Model):
    name = ndb.StringProperty(required=True)
    message = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        query = Comment.query()
        comment_data = query.fetch()
        template_vars = {'comments': comment_data}
        template = jinja2_environment.get_template('templates/index.html')
        self.response.write(template.render(template_vars))

class CommentCreateHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        message = self.request.get('message')
        current_date = datetime.datetime.now()
        comment = Comment(name=name, message=message)
        comment.created_date = current_date
        comment.put()
        self.redirect("/")

class CommentViewHandler(webapp2.RequestHandler):
    def get(self):
        comment_id = self.request.get('comment_id')
        comment = Comment.get_by_id(int(comment_id))
        template_vars = {'comment': comment }
        template = jinja2_environment.get_template('templates/index.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/comment/create', CommentCreateHandler)
], debug=True)

jinja2_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
