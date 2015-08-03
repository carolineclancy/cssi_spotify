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
        term="banana+pancakes"
        term_type="track"
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type={}&limit=1".format(term, term_type))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        entry_query = AddSongs.query()
        entry_data = entry_query.fetch()
        template = JINJA_ENVIRONMENT.get_template('index.html')

        self.response.write(template.render({'songs':entry_data, 'spotify': parsed_spotify_dictionary}))
        
    def post(self):
        vote = int(self.request.get('vote'))
        song_url_key = self.request.get('song_url_key')
        song_key = ndb.Key(urlsafe=song_url_key)
        song = song_key.get()
        song.votes_of_song = song.votes_of_song + vote
        song.put()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(t

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








# {
#   "tracks" : {
#     "href" : "https://api.spotify.com/v1/search?query=banana+pancakes&offset=1&limit=1&type=track",
#     "items" : [ {
#       "album" : {
#         "album_type" : "album",
#         "available_markets" : [ "CA", "US" ],
#         "external_urls" : {
#           "spotify" : "https://open.spotify.com/album/7tTc46dNdE6GGuiQsssWxo"
#         },
#         "href" : "https://api.spotify.com/v1/albums/7tTc46dNdE6GGuiQsssWxo",
#         "id" : "7tTc46dNdE6GGuiQsssWxo",
#         "images" : [ {
#           "height" : 576,
#           "url" : "https://i.scdn.co/image/72d78924e506cb6fd12ac77c5f4a0e3fa1de6880",
#           "width" : 640
#         }, {
#           "height" : 270,
#           "url" : "https://i.scdn.co/image/ce6d9d7a12b237eb0ca3a59088f4c8a3d5e94fc3",
#           "width" : 300
#         }, {
#           "height" : 58,
#           "url" : "https://i.scdn.co/image/1f479656718ae130e95464c4b136fbcb633a992f",
#           "width" : 64
#         } ],
#         "name" : "In Between Dreams",
#         "type" : "album",
#         "uri" : "spotify:album:7tTc46dNdE6GGuiQsssWxo"
#       },
#       "artists" : [ {
#         "external_urls" : {
#           "spotify" : "https://open.spotify.com/artist/3GBPw9NK25X1Wt2OUvOwY3"
#         },
#         "href" : "https://api.spotify.com/v1/artists/3GBPw9NK25X1Wt2OUvOwY3",
#         "id" : "3GBPw9NK25X1Wt2OUvOwY3",
#         "name" : "Jack Johnson",
#         "type" : "artist",
#         "uri" : "spotify:artist:3GBPw9NK25X1Wt2OUvOwY3"
#       } ],
#       "available_markets" : [ "CA", "US" ],
#       "disc_number" : 1,
#       "duration_ms" : 191906,
#       "explicit" : false,
#       "external_ids" : {
#         "isrc" : "USMC60400032"
#       },
#       "external_urls" : {
#         "spotify" : "https://open.spotify.com/track/451GvHwY99NKV4zdKPRWmv"
#       },
#       "href" : "https://api.spotify.com/v1/tracks/451GvHwY99NKV4zdKPRWmv",
#       "id" : "451GvHwY99NKV4zdKPRWmv",
#       "name" : "Banana Pancakes",
#       "popularity" : 74,
#       "preview_url" : "https://p.scdn.co/mp3-preview/bcda641ba7f9bfcb8a50be1b4260b2fcc17e3f02",
#       "track_number" : 3,
#       "type" : "track",
#       "uri" : "spotify:track:451GvHwY99NKV4zdKPRWmv"
#     } ],
#     "limit" : 1,
#     "next" : "https://api.spotify.com/v1/search?query=banana+pancakes&offset=2&limit=1&type=track",
#     "offset" : 1,
#     "previous" : "https://api.spotify.com/v1/search?query=banana+pancakes&offset=0&limit=1&type=track",
#     "total" : 80
#   }
# }
