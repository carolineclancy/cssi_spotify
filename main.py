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
import ast
from google.appengine.api import users

urlfetch.set_default_fetch_deadline(45)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Accounts(ndb.Model):
    user = ndb.UserProperty(required=True)
    ID = ndb.StringProperty(required=True)
    user_name = ndb.StringProperty(required=True)
    voted = ndb.StringProperty()

class UserVotes(ndb.Model):
    song_key = ndb.StringProperty(required=True)
    user_ID = ndb.StringProperty(required=True)
    vote_type = ndb.IntegerProperty(required=True)

class AddSongs(ndb.Model):
    song_name = ndb.StringProperty(required=True)
    votes_of_song = ndb.IntegerProperty(required=True)
    search_q = ndb.StringProperty(required=False)
    iframe_id = ndb.StringProperty(required=True)
    artist = ndb.StringProperty(required=True)
    iframes_var = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #login
        user = users.get_current_user()
        logout = ""
        login = ""
        if user:
            logout = ("{}").format(users.create_logout_url('/logout'))
            q = ndb.gql('SELECT * FROM Accounts WHERE ID = :1', user.user_id())
        else:
            login = users.create_login_url('/woohoo')

        #get database songs
        entry_query = AddSongs.query().order(-AddSongs.votes_of_song)
        entry_data = entry_query.fetch()

        #spotify
        # searches spotify for the song a user searched
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        #renders template
        iframes_var = []
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'songs':entry_data, 'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'logout': logout, "login": login}))

    def post(self):
        #check loggin system
        user = users.get_current_user()
        if user == None:
            self.response.out.write("Vote Failed")
            return
        print user
        #gets account ID
        account_query = Accounts.query()
        account_filter = account_query.filter(Accounts.user == user)
        account_ID = account_filter.fetch() #gets ID for account
        account_ID = account_ID[0].ID

        #voting system
        song_vote_count = self.request.get('vote')
        song_url_key = self.request.get('song_url_key')
        song_key = ndb.Key(urlsafe=song_url_key) #get song key
        song = song_key.get()
        vote_query = UserVotes.query()
        vote_filter = vote_query.filter(UserVotes.song_key == song_url_key).filter(UserVotes.user_ID == str(account_ID))
        vote_data = vote_filter.fetch()
        vote_data_length = len(vote_data)
        print vote_data
        if vote_data_length == 0:
            song.votes_of_song = song.votes_of_song + int(song_vote_count)
            song.put()
            new_voter = UserVotes(song_key=song_url_key, user_ID=account_ID, vote_type=int(song_vote_count))
            new_voter.put()
            print new_voter
        else:
            previous_vote = vote_data[0].vote_type
            if previous_vote == int(song_vote_count):
                self.response.out.write('Double Vote Failed')
                return
            vote_data[0].vote_type += int(song_vote_count)
            vote_data[0].put()

        #spotify
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(AddSongs.search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        #limit each vote to 1
        self.response.out.write('Vote Success')

        #render template
        # template = JINJA_ENVIRONMENT.get_template('index.html')
        # iframes_var = []
        # self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var}))
        # self.redirect('/')

class AddSongHandler(webapp2.RequestHandler):
    def get(self):
        #check loggin
        user = users.get_current_user()
        login = ""
        if user == None:
            login = users.create_login_url()

        #serach for song
        search_term = self.request.get('search_term')
        search_q = search_term.replace(" ", "+")
        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        template = JINJA_ENVIRONMENT.get_template('add_song.html')
        iframes_var = []

        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var': iframes_var, 'user': user, 'login':login}))
    def post(self):
        search_term = self.request.get('search_term')
        search_q = search_term.replace(" ", "+")
        votes_of_song = 0

        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        spotify = parsed_spotify_dictionary

        iframes_var = []
        counter = 0
        for song in spotify["tracks"]["items"]:
            iframe_id = spotify["tracks"]["items"][counter]["uri"]

            artist = spotify["tracks"]["items"][counter]["artists"][0]["name"]
            song_name = spotify["tracks"]["items"][counter]["name"]
            added_song = AddSongs(song_name = song_name, votes_of_song = votes_of_song, search_q= search_q, iframe_id=iframe_id, artist=artist, iframes_var=iframes_var)
            added_song.put()
            counter += 1
        iframes_var = []

        template = JINJA_ENVIRONMENT.get_template('song_choice.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'search_q':search_q}))
        self.redirect('/choose')

class ChooseSongHandler(webapp2.RequestHandler):
    def get(self):
        song_choice = self.request.get('song_choice')

        entry_query = AddSongs.query().order(-AddSongs.date)
        entry_data = entry_query.fetch()

        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=10".format(entry_data[0].search_q))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)

        spotify = parsed_spotify_dictionary

        template = JINJA_ENVIRONMENT.get_template('song_choice.html')
        self.response.write(template.render({'spotify':spotify}))
    def post(self):
        song_choice = self.request.get('song_choice')
        song_choice = ast.literal_eval(song_choice)
        song_choice1 = song_choice['name']

        song_choice1 = song_choice1.replace(" ", "+")

        votes_of_song = 0

        spotify_data_source = urlfetch.fetch("https://api.spotify.com/v1/search?q={}&type=track&limit=1".format(song_choice1))
        spotify_json_content = spotify_data_source.content
        parsed_spotify_dictionary = json.loads(spotify_json_content)
        spotify = parsed_spotify_dictionary
        iframe_id = song_choice["uri"]
        iframes_var = []


        artist = song_choice["artists"][0]["name"]
        song_name = song_choice["name"]
        added_song = AddSongs(song_name = song_name, votes_of_song = votes_of_song, iframe_id=iframe_id, artist=artist, iframes_var=iframes_var)
        added_song.put()

        entry_query = AddSongs.query().order(-AddSongs.date)
        entry_data = entry_query.fetch(11)

        counter = 0
        for song in entry_data:
            if song.iframe_id != song_choice["uri"]:
                entry_data[counter].key.delete()
            counter += 1

        counter2 = 0
        for song in entry_data:
            if song.iframe_id == song_choice["uri"] and song != added_song:
                entry_data[counter2].key.delete()
            counter2 += 1

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'spotify':parsed_spotify_dictionary, 'iframes_var':iframes_var, 'song_choice':song_choice}))
        self.redirect('/')
# class RegisterHandler(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         user_query = Accounts.query(Accounts.user == user)
#         user_data = user_query.count()
#         if user_data >= 1:
#             self.redirect('/woohoo')
#         else:
#             template = JINJA_ENVIRONMENT.get_template('register.html')
#             self.response.write(template.render())
#     def post(self):
#         user_name = self.request.get('user_name')
#         user_query = Accounts.query()
#         # user_data = user_query.fetch()
#         ID = str(user_query.count())
#         user = users.get_current_user()
#         accounts = Accounts(user = user, user_name = user_name, ID=ID)
#         accounts.put()
#         template = JINJA_ENVIRONMENT.get_template('register.html')
#         self.response.write(template.render())
#         self.redirect('/woohoo')

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about_us.html')
        self.response.write(template.render())

class WooHoo(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('woohoo.html')
        self.response.write(template.render())

class Logout(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('logout.html')
        self.response.write(template.render())

class AboutJam(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about_jam.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_song', AddSongHandler),
    ('/choose', ChooseSongHandler),
    ('/about_us', AboutUs),
    # ('/register', RegisterHandler),
    ('/woohoo', WooHoo),
    ('/logout', Logout),
    ('/about_jam', AboutJam)

], debug=True)
