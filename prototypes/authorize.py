from dotenv import load_dotenv
import os, base64, json, random, webbrowser, secrets
from requests import post, get

from flask import Flask, request, session, abort, redirect, render_template_string

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 7200

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

def generateRangomString(n: int) -> str:
	charaters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
	string = ""
	for _ in range(n):
		string += charaters[random.randrange(0, len(charaters))]
	return string

def getAuthHeader(token):
	return {"Authorization": "Bearer " + token}

def requestAuthorization():
	url = "https://accounts.spotify.com/authorize"
	redirectURI = "http://127.0.0.1:5000/callback"

	state = generateRangomString(16)
	session["state"] = state
	scope = "playlist-read-private"

	completeURL = f"{url}?client_id={clientID}&response_type=code&redirect_uri={redirectURI}&state={state}&scope={scope}"
	webbrowser.open(completeURL)

def requestAccessToken():
	url = "https://accounts.spotify.com/api/token"
	redirectURI = "http://127.0.0.1:5000/callback"

	authString = f"{clientID}:{clientSecret}"
	authBytes = authString.encode("utf-8")
	authBase64 = str(base64.b64encode(authBytes), "utf-8")

	headers = {
		"Authorization" : "Basic " + authBase64,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data = {
		"grant_type": "authorization_code",
		"code": session.pop("authCode", None),
		"redirect_uri": redirectURI
	}

	result = post(url, headers=headers, data=data)
	jsonResult = json.loads(result.content)
	session["token"] = jsonResult["access_token"]
	session["refreshToken"] = jsonResult["refresh_token"]
	timeLimit = jsonResult["expires_in"]

def getPlaylists():
	url = "https://api.spotify.com/v1/me/playlists"
	headers = getAuthHeader(session.get("token"))
	result = get(url, headers=headers)
	jsonResult = json.loads(result.content)["items"]
	for index, song in enumerate(jsonResult):
		print(f"{index+1}. {song['name']}")

@app.route("/")
def home():
	requestAuthorization()
	return "Please click okay when you have connected to you Spotify."

@app.route("/callback")
def callback():
	authorizationCode = request.args.get("code")
	state = request.args.get("state")

	generatedState = session.pop("state", None)
	if state != generatedState:
		abort(403)
	session["authCode"] = authorizationCode
	requestAccessToken()
	getPlaylists()
	return "Please wait"


if __name__ == "__main__":
	app.run(debug=False)