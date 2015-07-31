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
import logging
import random
import jinja2
import os
import time

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('I am the King!!! <br/>')
        # self.response.write('<br/><a href=/math?left=7&right=14>Math with 7 and 14</a>')
        template_vars = {"timeofday": time.asctime()}
        template = jinja_environment.get_template('templates/hello.html')
        self.response.write(template.render(template_vars))

class FormHandler(webapp2.RequestHandler):
    def post(self):
        realname = self.request.get("realname")
        self.response.write("It Worked!! Name entered is: " + realname)

class CounterHandler(webapp2.RequestHandler):
    def get(self):
        s = self.request.GET['startvalue']
        for i in range(int(s), 101):
            self.response.write(i)
            self.response.write(' ')

class GetUpHandler(webapp2.RequestHandler):
    def get(self):
            time = random.randint(0, 12)
            self.response.write('You worked on coding for ')
            self.response.write(time)
            self.response.write(' hours. ')
            if time > 3:
                self.response.write('Everybody get up and stretch!!! - Rob')
            else:
                self.response.write('Keep Going!!!!')

class MathHandler(webapp2.RequestHandler):
    def get(self):
        left = self.request.GET['left']
        sign = self.request.GET['sign']
        right = self.request.GET['right']
        # logging.info('LEFT=' + left)
        # self.response.write("It Worked!! Name entered is: " + realname)
        # self.response.write(left)
        # self.response.write(sign)
        # self.response.write(right)
        # self.response.write(' = ')
        if sign == '+':
            answer = (float(left) + float(right))
        if sign == '-':
            answer = (float(left) - float(right))
        if sign == '*':
            answer = (float(left) * float(right))
        if sign == '/':
            answer = (float(left) / float(right))
        if sign == '%':
            answer = (float(left) % float(right))
        if sign == '^':
            answer = (pow(float(left), float(right))) #(left ** right)<--same
        expression = left + " " + sign + " " + right + " = "
        template_vars = {'ans': answer, 'exp': expression}
        template = jinja_environment.get_template('templates/answer.html')
        self.response.write(template.render(template_vars))
        self.response.write('<br/>')

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/count', CounterHandler),
    ('/stretch', GetUpHandler),
    ('/math', MathHandler),
    ('/formhandler', FormHandler)
], debug=True)
