from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import loader
from .test import SpotifyHandler, debug
import requests

CLIENT_ID = "34ec9869a8f046a4bfa5c349fdf64a79"
REDIRECT_URI = "http://127.0.0.1:8000/callback"

# Create your views here.


# TODO: Add humidity
def index(request):
    context = {

    }
    print('hi')
    # loads the html and adds the context and converts it into string to send it through HttpResponse
    return HttpResponse(loader.render_to_string("index.html", context, request))


# TODO: Add state param for security
# TODO: Remove show_dialog in prod
def spotify_login(request):
    url = "https://accounts.spotify.com/authorize"
    param = {
        'client_id': CLIENT_ID,
        'response_type': "code",
        'redirect_uri': REDIRECT_URI,
        'scope': "user-library-read user-follow-read user-read-private user-read-email",
        'show_dialog': "true"
    }
    login_url = requests.get(url, param).url
    return HttpResponsePermanentRedirect(login_url)


# add the case when the user denies access
# TODO: add client_id and client_secret as header
# TODO: Address error during callback page reload
def process_login(request):
    error = request.GET.get('error')
    if error:
        print(error)
        return redirect('index')

    code = request.GET.get('code')
    url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': "08aeb1d6e448481ab7911913a7e4fcf9"
    }
    response = requests.post(url, payload).json()
    access_token = response['access_token']

    refresh_token = response['refresh_token']
    print("{}\n\n".format(access_token))
    # TODO: Save user id and refresh token to user's database
    spotify_handler = SpotifyHandler(access_token, "rainy", True)
    return HttpResponse("<h1> Successful </h1>")


# TODO: Should be removed
def generate_access_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': "refresh_token",
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': "08aeb1d6e448481ab7911913a7e4fcf9"
    }
    response = requests.post(url, payload).json()
    print(response)
