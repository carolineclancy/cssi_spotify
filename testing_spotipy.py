import spotipy

def Test():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(lz_uri)
    global results_array
    results_array = []
    for track in results['tracks'][:10]:
        # print 'track    : ' + track['name']
        # print 'audio    : ' + track['preview_url']
        # print 'cover art: ' + track['album']['images'][0]['url']
        results_array.push("track: {} \n audio: {}".format(track['name'], track['preview_url']))
    return results_array
