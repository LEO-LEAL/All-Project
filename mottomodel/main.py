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

class Student(ndb.Model):
    name = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    club = ndb.StringProperty(required=False)
    attended_CSSI = ndb.BooleanProperty(required=False)
    created_date = ndb.DateTimeProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2_environment.get_template('templates/index.html')
        self.response.write(template.render())

class AddStudentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2_environment.get_template('templates/add_students.html')
        self.response.write(template.render())

class StudentCreateHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        school = self.request.get('school')
        club = self.request.get('club')
        attended_CSSI = self.request.get('attended_CSSI')
        current_date = datetime.datetime.now()
        if(attended_CSSI == 'on'):
            attended_CSSI_bool = True
        else:
            attended_CSSI_bool = False
        logging.info('ATTENDED_CSSI: ' + attended_CSSI)
        student = Student(name=name, school=school, club=club,
            attended_CSSI=attended_CSSI_bool)
        student.created_date = current_date
        student.put()
        self.response.write('Student was created')
        self.response.write('<a href = "/add_student">Add Student</a>')

class StudentListHandler(webapp2.RequestHandler):
    def get(self):
        query = Student.query()
        student_data = query.fetch()
        template_vars = {'students': student_data}
        template = jinja2_environment.get_template('templates/list_students.html')
        self.response.write(template.render(template_vars))

class StudentViewHandler(webapp2.RequestHandler):
    def get(self):
        student_id = self.request.get('student_id')
        student = Student.get_by_id(int(student_id))
        template_vars = {'student': student }
        template = jinja2_environment.get_template('templates/view_student.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_student', AddStudentHandler),
    ('/student/create', StudentCreateHandler),
    ('/student/list', StudentListHandler),
    ('/student/view', StudentViewHandler)
], debug=True)

jinja2_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
