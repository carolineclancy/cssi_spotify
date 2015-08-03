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
vendor.add('lib/urllib3')
import os
import jinja2


# import requests
# import spotipy
# import ssl
# import sys
# from google.appengine.api import urlfetch
# import urllib3

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def Test():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        return "track: {} \n audio: {}".format(track['name'], track['preview_url'])

class AddSongs(ndb.Model):
    song_name = ndb.StringProperty(required=True)
    artist_name = ndb.StringProperty(required=True)
    votes_of_song = ndb.IntegerProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        entry_query = AddSongs.query()
        entry_data = entry_query.fetch()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'songs':entry_data}))
    def post(self):
        vote = int(self.request.get('vote'))
        song_url_key = self.request.get('song_url_key')
        song_key = ndb.Key(urlsafe=song_url_key)
        song = song_key.get()
        song.votes_of_song = song.votes_of_song + vote
        song.put()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
        self.redirect('/')

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
