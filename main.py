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
    votes_of_song = ndb.IntegerProperty(required=True)
    search_q = ndb.StringProperty(required=False)
    iframe_id = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get database songs
        entry_query = AddSongs.query()
        entry_data = entry_query.fetch()
        #spotify

        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'songs':entry_data, 'spotify':parsed_spotify_dictionary}))
    def post(self):
        #voting system
        vote = int(self.request.get('vote'))
        song_url_key = self.request.get('song_url_key')
        song_key = ndb.Key(urlsafe=song_url_key)
        song = song_key.get()
        song.votes_of_song = song.votes_of_song + vote
        song.put()
        #spotify
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary}))
        self.redirect('/')

class AddSongHandler(webapp2.RequestHandler):
    def get(self):
        search_term = self.request.get('search_term')
        search_q = search_term.replace(" ", "+")
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)


        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary}))
    def post(self):
        #input song
        # song_name = self.request.get('name_of_song')
        # artist_name = self.request.get('artist_of_song')
        search_term = self.request.get('search_term')

        search_q = search_term.replace(" ", "+")

        votes_of_song = 0

        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        spotify = parsed_spotify_dictionary
        iframe_id = spotify["tracks"]["items"][0]["uri"]

        added_song = AddSongs(song_name = search_term, votes_of_song = votes_of_song, search_q= search_q, iframe_id=iframe_id)
        added_song.put()
        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary}))
        self.redirect('/')




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_song', AddSongHandler)
], debug=True)
