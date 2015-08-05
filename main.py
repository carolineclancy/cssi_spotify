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


class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about_us.html')
        self.response.write(template.render())

# class ChooseSongHandler(webapp2.RequestHandler):
#     def get(self):
#         search_term = self.request.get('search_term')
#         search_q = search_term.replace(" ", "+")
#         votes_of_song = 0
#         spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(search_q))
#         spotify_json_content = spotify_data_source.content
#         parsed_spotify_dictionary = json.loads(spotify_json_content)
#         spotify = parsed_spotify_dictionary
#         song_choice =
#         iframe_id = spotify["tracks"]["items"][song_choice]["uri"]
#         added_song = AddSongs(song_name = search_term, votes_of_song = votes_of_song, search_q= search_q, iframe_id=iframe_id)
#         added_song.put()
#         template = JINJA_ENVIRONMENT.get_template('add_song.html')
#         self.response.write(template.render({'spotify':parsed_spotify_dictionary}))
#     def post(self):
#          search_term = self.request.get('search_term')
#          search_q = search_term.replace(" ", "+")
#          votes_of_song = 0
#          spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(search_q))
#          spotify_json_content = spotify_data_source.content
#          parsed_spotify_dictionary = json.loads(spotify_json_content)
#          spotify = parsed_spotify_dictionary
#          song_choice =
#          iframe_id = spotify["tracks"]["items"][song_choice]["uri"]
#          added_song = AddSongs(song_name = search_term, votes_of_song = votes_of_song, search_q= search_q, iframe_id=iframe_id)
#          added_song.put()
#          template = JINJA_ENVIRONMENT.get_template('add_song.html')
#          self.response.write(template.render({'spotify':parsed_spotify_dictionary}))
#          self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_song', AddSongHandler),
    # ('/choose', ChooseSongHandler),
    ('/about_us', AboutUs)

], debug=True)




#
#
# {
#   "tracks" : {
#     "href" : "https://api.spotify.com/v1/search?query=Banana+Pancakes&offset=0&limit=20&type=track",
#     "items" : [ {
#       "album" : {
#         "album_type" : "album",
#         "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "IE", "IS", "IT", "LI", "LT", "LU", "LV", "MC", "MT", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SI", "SK", "SV", "TR", "TW", "UY" ],
#         "external_urls" : {
#           "spotify" : "https://open.spotify.com/album/2B9q4KPjOEYu885Keo9dfX"
#         },
#         "href" : "https://api.spotify.com/v1/albums/2B9q4KPjOEYu885Keo9dfX",
#         "id" : "2B9q4KPjOEYu885Keo9dfX",
#         "images" : [ {
#           "height" : 576,
#           "url" : "https://i.scdn.co/image/247a46eb5451173701b8596b67cb52196f9caaed",
#           "width" : 640
#         }, {
#           "height" : 270,
#           "url" : "https://i.scdn.co/image/0128dae92d47e8c51e11290ba91a6448e9dcd39a",
#           "width" : 300
#         }, {
#           "height" : 58,
#           "url" : "https://i.scdn.co/image/4a85cf4b33b27376a88b80ccb09cdd8da3d37631",
#           "width" : 64
#         } ],
#         "name" : "In Between Dreams",
#         "type" : "album",
#         "uri" : "spotify:album:2B9q4KPjOEYu885Keo9dfX"
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
#       "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "IE", "IS", "IT", "LI", "LT", "LU", "LV", "MC", "MT", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SI", "SK", "SV", "TR", "TW", "UY" ],
#       "disc_number" : 1,
#       "duration_ms" : 191906,
#       "explicit" : false,
#       "external_ids" : {
#         "isrc" : "USMC60400032"
#       },
#       "external_urls" : {
#         "spotify" : "https://open.spotify.com/track/0BgbobvykXxEvxo2HhCuvM"
#       },
#       "href" : "https://api.spotify.com/v1/tracks/0BgbobvykXxEvxo2HhCuvM",
#       "id" : "0BgbobvykXxEvxo2HhCuvM",
#       "name" : "Banana Pancakes",
#       "popularity" : 75,
#       "preview_url" : "https://p.scdn.co/mp3-preview/6edb1319171ca378975022a86b84d0719e467311",
#       "track_number" : 3,
#       "type" : "track",
#       "uri" : "spotify:track:0BgbobvykXxEvxo2HhCuvM"
#     }, {
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
#     }, {
