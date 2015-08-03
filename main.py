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
import os
import jinja2
import json
from google.appengine.api import urlfetch


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class AddSongs(ndb.Model):
    song_name = ndb.StringProperty(required=True)
    artist_name = ndb.StringProperty(required=True)
    votes_of_song = ndb.IntegerProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        term="jack+johnson"
        term_type="artist"
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type={}&limit=1".format(term, term_type))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        entry_query = AddSongs.query()
        entry_data = entry_query.fetch()
        template = JINJA_ENVIRONMENT.get_template('index.html')

        self.response.write(template.render({'songs':entry_data, 'spotify': parsed_spotify_dictionary}))

class AddSongHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        self.response.write(template.render())
    def post(self):
        song_name = self.request.get('name_of_song')
        artist_name = self.request.get('artist_of_song')
        votes_of_song = 0
        added_song = AddSongs(song_name = song_name, artist_name = artist_name, votes_of_song = votes_of_song)
        added_song.put()
        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        self.response.write(template.render())
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_song', AddSongHandler)
], debug=True)
