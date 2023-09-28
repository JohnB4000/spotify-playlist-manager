from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

clientID: str = os.getenv("CLIENT_ID")
clientSecret: str = os.getenv("CLIENT_SECRET")

def getToken() -> str:
	authString: str = f"{clientID}:{clientSecret}"
	authBytes: bytes = authString.encode("utf-8")
	authBase64: str = str(base64.b64encode(authBytes), "utf-8")

	url: str = "https://accounts.spotify.com/api/token"
	headers = {
		"Authorization" : "Basic " + authBase64,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data = {"grant_type": "client_credentials"}
	result = post(url, headers=headers, data=data)
	jsonResult = json.loads(result.content)
	token = jsonResult["access_token"]
	return token

def getAuthHeader(token):
	return {"Authorization": "Bearer " + token}

def searchForArtist(token, artistName):
	url = "https://api.spotify.com/v1/search"
	headers = getAuthHeader(token)
	query = f"?q={artistName}&type=artist&limit=1"

	queryUrl = url + query

	result = get(queryUrl, headers=headers)
	jsonResult = json.loads(result.content)["artists"]["items"]
	if len(jsonResult) == 0:
		print("No artist with this name exists.")
		return None
	return jsonResult[0]

def getSongsByArtist(token, artistID):
	url = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?country=GB"
	headers = getAuthHeader(token)

	result = get(url, headers=headers)
	jsonResult = json.loads(result.content)["tracks"]
	return jsonResult


token = getToken()
result = searchForArtist(token, "Foals")
artistID = result["id"]
songs = getSongsByArtist(token, artistID)

for index, song in enumerate(songs):
	print(f"{index+1}. {song['name']}")