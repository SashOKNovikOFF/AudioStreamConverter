def get_album_and_track_from_spotify_url(urlname):

    from urllib.parse import unquote, urlparse
    from pathlib import PurePosixPath
    ids = PurePosixPath(unquote(urlparse(urlname).path)).parts
    if len(ids) == 3 and ids[1] == 'track':
        return ids[2]
    else:
        return ""


def get_artist_and_title_from_spotify(track_id):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    uri = 'spotify:track:' + track_id
    track = sp.track(uri)
    return track['artists'][0]['name'], track['name']


def get_url_from_yandex_by_artist_and_title(artist, title):
    from yandex_music.utils.request import Request
    from yandex_music import Client

    request = Request(proxy_url='socks5://socks.zaborona.help:1488')
    client = Client(request=request)
    query = artist + " " + title
    search_result = client.search(query)

    if len(search_result['tracks']['results']) != 0:
        best = search_result['tracks']['results'][0]
        full_id = best.track_id.split(':')
        album_id = full_id[1]
        track_id = full_id[0]
        return "https://music.yandex.ru/album/" + album_id + "/track/" + track_id
    else:
        return "None"


def get_album_and_track_from_yandex_url(urlname):

    from urllib.parse import unquote, urlparse
    from pathlib import PurePosixPath
    ids = PurePosixPath(unquote(urlparse(urlname).path)).parts
    if len(ids) == 5 and ids[1] == 'album' and ids[3] == 'track':
        return ids[2], ids[4]
    elif len(ids) == 3 and ids[1] == 'track':
        return "", ids[2]
    else:
        return "", ""


def get_artist_and_title_from_yandex(album_id, track_id):
    from yandex_music import Client

    client = Client()
    if album_id == "":
        track_info = client.tracks(track_id)
    else:
        trackID = str(track_id) + ':' + str(album_id)
        track_info = client.tracks(trackID)
    title, artist = track_info[0].title, track_info[0].artists_name()[0]

    return artist, title


def get_url_from_spotify_by_artist_and_title(title, artist):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    query = artist + " " + title
    sp_data = sp.search(q=query, type="track", limit=10)

    items = sp_data['tracks']['items']
    if len(items) > 0:
        ext_url = items[0]['external_urls']['spotify']
        return ext_url
