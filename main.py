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

urlfetch.set_default_fetch_deadline(45)
# iframes_var = []
# global iframes_var
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AddSongs(ndb.Model):
    song_name = ndb.StringProperty(required=True)
    votes_of_song = ndb.IntegerProperty(required=True)
    search_q = ndb.StringProperty(required=False)
    iframe_id = ndb.StringProperty(required=True)
    artist = ndb.StringProperty(required=True)
    iframes_var = ndb.StringProperty(repeated=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get database songs
        entry_query = AddSongs.query().order(-AddSongs.votes_of_song)

        entry_data = entry_query.fetch()
        #spotify
        # searches spotify for the song a user searched
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        iframes_var = []
        counter = 0

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'songs':entry_data, 'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'counter':counter}))

    def post(self):
        #voting system
        song_vote_count = self.request.get('vote')
        song_url_key = self.request.get('song_url_key')
        song_key = ndb.Key(urlsafe=song_url_key)
        song = song_key.get()
        song.votes_of_song = song.votes_of_song +  int(song_vote_count)
        song.put()
        #spotify
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        iframes_var = []
        counter = 0

        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'counter':counter}))
        self.redirect('/')

class AddSongHandler(webapp2.RequestHandler):
    def get(self):
        search_term = self.request.get('search_term')
        search_q = search_term.replace(" ", "+")
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        iframes_var = []
        counter = 0
        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var': iframes_var, 'counter':counter}))
    def post(self):
        search_term = self.request.get('search_term')
        search_q = search_term.replace(" ", "+")
        votes_of_song = 0
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        spotify = parsed_spotify_dictionary
        iframe_id = spotify["tracks"]["items"][0]["uri"]
        iframes_var = []
        counter = 0


        artist = spotify["tracks"]["items"][0]["artists"][0]["name"]
        song_name = spotify["tracks"]["items"][0]["name"]
        added_song = AddSongs(song_name = song_name, votes_of_song = votes_of_song, search_q= search_q, iframe_id=iframe_id, artist=artist, iframes_var=iframes_var)
        added_song.put()

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'counter':counter}))
        self.redirect('/')

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render())
        
class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about_us.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_song', AddSongHandler),
    ('/register',RegisterHandler),
    ('/about_us', AboutUs)

], debug=True)
