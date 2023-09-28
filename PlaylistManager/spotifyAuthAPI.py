from dotenv import load_dotenv
import os, json, random, base64
from requests import post, get
from typing import Tuple

from flask import session, redirect


class SpotifyAuthURLs:
	"""Used to store Spotify urls and the redirect URI."""

	APP_SCOPE = "playlist-read-private user-read-email user-top-read"

	APP_REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"

	REQUEST_USER_AUTHORIZATION = "https://accounts.spotify.com/authorize"
	REQUEST_ACCESS_TOKEN = "https://accounts.spotify.com/api/token"



def build_request_user_auth_url(client_id: str, state: str) -> str:
	"""Used to build the request user request authorization url."""
	
	return f"{SpotifyAuthURLs.REQUEST_USER_AUTHORIZATION}?client_id={client_id}&response_type=code&redirect_uri={SpotifyAuthURLs.APP_REDIRECT_URI}&state={state}&scope={SpotifyAuthURLs.APP_SCOPE}"

def build_request_access_token_url(client_id: str, client_secret: str) -> Tuple[str, dict[str, str], dict[str, str]]:
	"""Used to build the request access token url."""
	
	auth_base64 = str(base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")), "utf-8")
	headers = {
		"Authorization" : "Basic " + auth_base64,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data = {
		"grant_type": "authorization_code",
		"code": session.pop("auth_code", None),
		"redirect_uri": SpotifyAuthURLs.APP_REDIRECT_URI
	}
	return SpotifyAuthURLs.REQUEST_ACCESS_TOKEN, headers, data


def load_spotify_app_details() -> Tuple[str]:
	"""Loads in the Client ID and Client Secret from the .env file."""

	load_dotenv()
	client_id = os.getenv("CLIENT_ID")
	client_secret = os.getenv("CLIENT_SECRET")
	return client_id, client_secret

def generate_random_string(n: int) -> str:
	"""Generates a random 'n' long string, (A-Z, a-z, 0-9)."""

	characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
	return ''.join([characters[random.randrange(0, len(characters))] for _ in range(n)])

def get_auth_header(token: str) -> dict[str, str]:
	"""Formats the authorization token header."""

	return {"Authorization": "Bearer " + token}


def request_authorization() -> None:
	"""Requests user authorization from Spotify."""

	client_id, _ = load_spotify_app_details()
	state = generate_random_string(16)
	session["state"] = state
	return build_request_user_auth_url(client_id, state)

def request_access_token() -> None:
	"""Requests a access token and stores the token and refresh token in session variables 'token' and 'refresh_token'."""

	client_id, client_secret = load_spotify_app_details()
	url, headers, data = build_request_access_token_url(client_id, client_secret)
	result = post(url, headers=headers, data=data)
	json_result = json.loads(result.content)
	session["token"] = json_result["access_token"]
	session["refresh_token"] = json_result["refresh_token"]