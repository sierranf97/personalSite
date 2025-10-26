from dotenv import load_dotenv, dotenv_values
import os
import requests
import base64
from flask import render_template

load_dotenv('/home/sierranf97/personalSite/.env')
load_dotenv()
my_secrets = dotenv_values(".env")
print(my_secrets)

TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"

class SpotifyReq:
    def __init__(self):
        # self.id = my_secrets['CLIENT_ID']
        # self.secret = my_secrets['CLIENT_SECRET']
        # self.redirect = my_secrets['REDIRECT_URI']
        self.id = os.getenv('CLIENT_ID')
        self.secret = os.getenv('CLIENT_SECRET')
        self.redirect = os.getenv('REDIRECT_URI')


    def search(self, song_title, artist):
        # Get access token
        encoded = base64.b64encode((self.id + ":" + self.secret).encode("ascii")).decode("ascii")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + encoded
        }

        payload = {
            "grant_type": "client_credentials"
        }

        response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
        auth_token = response.json()['access_token']

        # Search API
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        query = ""
        if song_title != "":
            query += f"track:'{song_title}' "
        if artist != "":
            query += f"artist:'{artist}' "

        params = {
            "q": query,
            "type": "track",
        }

        response = requests.get(url=SEARCH_ENDPOINT, headers=headers, params=params)

        try:
            preview_url = response.json()["tracks"]["items"][0]["preview_url"]
            tracks = response.json()["tracks"]["items"]
            song_url = tracks[0]['external_urls']['spotify']
            print(song_url)
            if preview_url is None:
                return render_template("songerror.html")
            else:
                return preview_url
        except IndexError:
            return render_template("songerror.html")
        except ValueError:
            return render_template("songerror.html")
