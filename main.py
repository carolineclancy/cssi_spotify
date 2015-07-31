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
import spotipy
import requests

def Test():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        return "track: {} \n audio: " 'track    : ' + track['name']
        print 'audio    : ' + track['preview_url']
        print 'cover art: ' + track['album']['images'][0]['url']


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(Test())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
