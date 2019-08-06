# TODO: remove debug statements
import requests
from functools import reduce


class SpotifyHandler:
    def __init__(self, access_token, weather, is_daylight, user_id=None):
        self.access_token = access_token
        self.weather = weather
        self.isDaylight = is_daylight
        # TODO: Content Type??
        self.header = {
            'Authorization': "Bearer " + self.access_token
        }
        # TODO: Save user id and refresh token to user's database
        self.user_id = user_id if user_id else self.__get_user_id()
        self.get_personalized_playlist()

    def __get_user_id(self):
        endpoint_url = "https://api.spotify.com/v1/me"
        response = requests.get(endpoint_url, headers=self.header).json()
        debug("\n\n", response, response['id'])
        return response['id']

    def get_personalized_playlist(self):
        track_ids = []
        final_track_ids = []
        endpoint_url = "https://api.spotify.com/v1/audio-features"
        params = {
            'limit': '50',
        }
        self.__get_user_tracks(track_ids, params)
        self.__get_user_albums(track_ids, params)
        self.__get_user_playlist(track_ids, params)
        debug(len(track_ids))
        track_ids_str = reduce(lambda x, y: "" + x + ',' + y, track_ids)
        debug('\n', track_ids_str)
        params1 = {
            'ids':  track_ids_str
        }
        # TODO: Address for id max limit(100) issue
        response = requests.get(endpoint_url, params1, headers=self.header).json()
        for track_features in response['audio_features']:
            final_track_ids.append(self.__personalize(track_features))
        debug('\n', final_track_ids)

    def __get_user_tracks(self, track_ids, params):
        debug(len(track_ids))
        endpoint_url = "https://api.spotify.com/v1/me/tracks"
        while 1:
            response = requests.get(endpoint_url, params, headers=self.header).json()
            for obj in response['items']:
                if obj['track']['id'] not in track_ids:
                    track_ids.append(obj['track']['id'])
            if response['next']:
                endpoint_url = response['next']
            else:
                break
        debug('\nHere1:', track_ids)

    def __get_user_albums(self, tracks_ids, params):
        endpoint_url = 'https://api.spotify.com/v1/me/albums'
        while 1:
            response = requests.get(endpoint_url, params, headers=self.header).json()
            for albums in response['items']:
                for tracks in albums['album']['tracks']['items']:
                    if tracks['id'] not in tracks_ids:
                        tracks_ids.append(tracks['id'])
            if response['next']:
                endpoint_url = response['next']
            else:
                break
        debug('\nHEre2:', tracks_ids)

    def __get_user_playlist(self, track_ids, params):
        endpoint_url = "https://api.spotify.com/v1/me/playlists"
        # TODO: Address followed amd private playlist issue
        #       followed playlist not showing up
        while 1:
            response = requests.get(endpoint_url, params, headers=self.header).json()
            for playlist in response['items']:
                self.__get_distinct_tracks(track_ids, playlist['tracks']['href'])
            if response['next']:
                endpoint_url = response['next']
            else:
                break
        debug('\nHere3:', track_ids)

    # deals with list of tracks object
    def __get_distinct_tracks(self, track_ids, endpoint_url):
        params = {
            'limit': '100'
        }
        while 1:
            response = requests.get(endpoint_url, params, headers=self.header).json()
            for obj in response['items']:
                if obj['track']['id'] not in track_ids:
                    track_ids.append(obj['track']['id'])
            if response['next']:
                endpoint_url = response['next']
            else:
                break
        debug("\n", len(track_ids))

    # TODO: Need to implement functionality
    def __personalize(self, track_features):
        debug(track_features)
        return track_features['id']


def debug(str, *args):
    print(str)
    for item in args:
        if item:
            print(item)
