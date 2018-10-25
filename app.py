from flask import Flask
from flask_cors import CORS
from flask import request

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOauthError
from spotipy import SpotifyException
import json

import logging
import sys

import time

app = Flask(__name__)
CORS(app)

# LOGGING DEF
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('ml-artist-discovery')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

def get_sp_client():
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp


@app.route("/api/search_artists", methods=["POST"])
def search_artists():
    # artist = request.args.get("artist", "")

    artist = request.values.get("artist", "")

    logger.debug("Artista cercato: %s", artist)

    ms_results = []

    if artist.strip() != "":
        # time.sleep(5)

        sp = get_sp_client()

        try:
            results = sp.search(q="artist:" + artist, type="artist")

            artists = results["artists"]["items"]

            for artist in artists:
                ms_result = {
                    "uri": artist["uri"],
                    "name": artist["name"],
                    "image": artist["images"][0]["url"] if len(artist["images"]) > 0 else "",
                    "followers": artist["followers"]["total"]
                }

                ms_results.append(ms_result)

        except SpotifyException as spEx:
            logger.error("La ricerca ha restituito un errore! %s[%s]", spEx.message, spEx.msg)

        except SpotifyOauthError as oauthError:
            logger.error("Errore di autenticazione! %s", oauthError.message)

    jsonResponse = json.dumps(ms_results, indent=True)

    response = app.response_class(
        response=jsonResponse,
        status=200,
        mimetype="application/json")

    return response


@app.route("/api/artist/<artist_uri>", methods=["GET"])
def get_artists(artist_uri=None):
    ms_result = {}

    logger.debug("Recupero delle informazioni di dettaglio dell'artista. Uri: %s", artist_uri)

    if artist_uri is not None and artist_uri.strip() != "":
        # time.sleep(5)
        sp = get_sp_client()

        try:
            artist = sp.artist(artist_uri)
            ms_result = artist

        except SpotifyException as spEx:
            logger.error("L'artista non esiste! %s[%s]", spEx.message, spEx.msg)

        except SpotifyOauthError as oauthError:
            logger.error("Errore di autenticazione! %s", oauthError.message)

    jsonResponse = json.dumps(ms_result, indent=True)

    response = app.response_class(
        response=jsonResponse,
        status=200,
        mimetype="application/json")

    return response


if __name__ == '__main__':
    app.run()
