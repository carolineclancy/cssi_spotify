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
from google.appengine.ext import ndb
from google.appengine.ext import vendor
vendor.add('lib/spotipy')
vendor.add('lib/requests')
import os
import jinja2
import requests
import spotipy
import ssl
import sys
from google.appengine.api import urlfetch



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Song(ndb.Model):
    song_title = ndb.StringProperty(required=True)
    song_artist = ndb.StringProperty(required=False)



def Test():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        return "track: {} \n audio: {}".format(track['name'], track['preview_url'])


class MainHandler(webapp2.RequestHandler):
    def get(self):
        g = requests.get('http://www.google.com')
        self.response.write(g.text)
        self.response.write(Test())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
