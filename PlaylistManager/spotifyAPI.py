from requests import get
from json import loads

from flask import session

from . import spotifyAuthAPI


class SpotifyAPIURLs:
	GET_CURRENT_USER_PROFILE = "https://api.spotify.com/v1/me"
	GET_CURRENT_USER_PLAYLISTS = "https://api.spotify.com/v1/me/playlists"
	GET_CURRENT_USER_TOP_ITEMS = "https://api.spotify.com/v1/me/top"
	GET_PLAYLIST = "https://api.spotify.com/v1/playlists"

class SpotifyUserTopItems:
	class Types:
		ARTISTS = "artists"
		SONGS = "tracks"

	class TimeRange:
		SHORT = "short_term"
		MEDIUM = "medium_term"
		LONG = "long_term"
		ALL = "all"

def get_user_profile() -> dict[str, any]:
	headers = spotifyAuthAPI.get_auth_header(session.get("token"))
	response = get(SpotifyAPIURLs.GET_CURRENT_USER_PROFILE, headers=headers)
	return loads(response.content)

def get_current_users_playlists(limit: int = 50, offset: int = 0) -> dict[str, any]:
	headers = spotifyAuthAPI.get_auth_header(session.get("token"))
	url = f"{SpotifyAPIURLs.GET_CURRENT_USER_PLAYLISTS}?limit={limit}&offset={offset}"
	response = get(url, headers=headers)
	return loads(response.content)["items"]

def get_users_top_items(item_type: str, time_range: str, limit: int = 20, offset: int = 0):
	if time_range == SpotifyUserTopItems.TimeRange.ALL:
		ranges = ["short_term", "medium_term", "long_term"]
		top_items = [get_users_top_items(item_type, range, limit, offset) for range in ranges]
		return top_items
	headers = spotifyAuthAPI.get_auth_header(session.get("token"))
	url = f"{SpotifyAPIURLs.GET_CURRENT_USER_TOP_ITEMS}/{item_type}?time_range={time_range}&limit={limit}&offset={offset}"
	response = get(url, headers=headers)
	return loads(response.content)['items']

def get_playlist_details(playlist_id: int, market: str = "GB"):
	headers = spotifyAuthAPI.get_auth_header(session.get("token"))
	url = f"{SpotifyAPIURLs.GET_PLAYLIST}/{playlist_id}?market={market}"
	response = get(url, headers=headers)
	return loads(response.content)

def get_playlist_tracks(playlist_id: int, market: str = "GB", fields: str = "", limit: int = 50, offset: int = 0):
	tracks = []
	headers = spotifyAuthAPI.get_auth_header(session.get("token"))
	if fields is "":
		fields = "next,items(added_at,track(id,name,artists,duration_ms,album(name,release_date,images)))"
	next_url = f"{SpotifyAPIURLs.GET_PLAYLIST}/{playlist_id}/tracks?market={market}&fields={fields}&limit={limit}&offset={offset}"
	while next_url is not None:
		response = get(next_url, headers=headers)
		jsonResponse = loads(response.content)
		tracks.extend(jsonResponse['items'])
		next_url = jsonResponse['next']
	return tracks