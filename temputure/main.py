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
import urllib2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
import logging
import datetime

class Temperature(ndb.Model):
    temperature = ndb.IntegerProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    created = ndb.DateTimeProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        query = Temperature.query()
        data = query.fetch()

class TemperatureHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2_enviroment.get_template("templates/index.html")
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        url = ('http://api.openweathermap.org/data/2.5/weather?'
        'lat=%s&lon=%s&units=Imperial&APPID=883c191fd8d3d4a18ed700f5f65dcfd4' % (lat, lon))
        string = urllib2.urlopen(url).read()
        dictionary = json.loads(string)
        # logging.info(dictionary)
        if lat == "" or lon == "":
            form = True
            howhot = "Waiting for temperature data"
        else:
            form = False
            howhot = dictionary['main']['temp']
            temp = Temperature(temperature = int(howhot), latitude=float(lat), longitude=float(lon),
                created=datetime.datetime.now())
            temp.put()

        template_vars = {'temperature':howhot, 'form': form}
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', TemperatureHandler),
    ('/main', MainHandler)

], debug=True)

jinja2_enviroment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname (__file__)))
