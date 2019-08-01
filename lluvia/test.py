import requests


class SpotifyHandler:
    def __init__(self, access_token, weather, is_daylight, user_id=None):
        self.access_token = access_token
        self.weather = weather
        self.isDaylight = is_daylight
        self.header = {
            'Authorization': "Bearer " + self.access_token
        }
        # TODO: Save user id and refresh token to user's database
        self.user_id = user_id if user_id else self.__get_user_id()
        # remove this line
        self.__get_user_playlist()

    def __get_user_id(self):
        endpoint_url = "https://api.spotify.com/v1/me"
        response = requests.get(endpoint_url, headers=self.header).json()
        debug("\n\n", response, response['id'])
        return response['id']

    def __get_user_playlist(self):
        track_ids = []
        endpoint_url = "https://api.spotify.com/v1/me/playlists"
        # TODO: Address followed amd private playlist issue
        #       followed playlist not showing up
        params = {
            'limit': '50',
        }
        while 1:
            response = requests.get(endpoint_url, params, headers=self.header).json()
            debug("\n", response)
            for playlist in response['items']:
                self.__get_distinct_tracks(track_ids, playlist['tracks']['href'])
            if response['next']:
                endpoint_url = response['next']
            else:
                break
        return track_ids

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


def debug(str, *args):
    print(str)
    for item in args:
        if item:
            print(item)
