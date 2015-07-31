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
import webapp2
import jinja2
import os

jinja2_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        entry = jinja2_environment.get_template('templates/entry.html')
        self.response.write(entry.render())

class ResponseHandler(webapp2.RequestHandler):
    def post(self):
        # team_members = {
        #     'Eleanor': {'college':'CalPolySLO'},
        #     'Frank': {'college':'UCI'},
        #     'Yelena': {'college':'Stanford'},
        #     'Stepnanie': {'college':'Occidental'},
        #     'Leo': {'college':'UCI'}
        #     }
        #
        # noun1 = self.request.get('noun1')
        # pluralnoun1 = self.request.get('pluralnoun1')
        # adj1 = self.request.get('adj1')
        # verb1 = self.request.get('verb1')
        # verb2 = self.request.get('verb2')
        # verb3 = self.request.get('verb3')
        # verb4 = self.request.get('verb4')
        # pluralnoun2 = self.request.get('pluralnoun2')
        # adj2 = self.request.get('adj2')
        # verb5 = self.request.get('verb5')
        # verb6 = self.request.get('verb6')
        # verb7 = self.request.get('verb7')
        # noun2 = self.request.get('noun2')
        # dict_words = {'pluralnoun1': pluralnoun1, 'noun1': noun1, 'adj1': adj1,
        #  'verb1': verb1, 'verb2': verb2, 'verb3': verb3, 'verb4': verb4,
        #  'pluralnoun2': pluralnoun2, 'adj2': adj2, 'verb5': verb5, 'verb6': verb6,
        #  'verb7': verb7, 'noun2': noun2, 'team_members': team_members}
        page = jinja2_environment.get_template('templates/response.html')
        self.response.write(page.render(self.request.POST))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/response', ResponseHandler)
], debug=True)
