from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from PlaylistManager.db import get_db

from .auth import login_required
from . import spotifyAPI

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/", methods=("GET", "POST"))
@login_required
def playlists():
	playlists = spotifyAPI.get_current_users_playlists()
	return render_template("dashboard/playlists.html", playlists=playlists, user_spotify_id=session.get("user_spotify_id"))

@bp.route("/statistics", methods=("GET", "POST"))
@login_required
def statistics():
	top_songs = spotifyAPI.get_users_top_items(spotifyAPI.SpotifyUserTopItems.Types.SONGS, spotifyAPI.SpotifyUserTopItems.TimeRange.ALL, 10)
	top_artists = spotifyAPI.get_users_top_items(spotifyAPI.SpotifyUserTopItems.Types.ARTISTS, spotifyAPI.SpotifyUserTopItems.TimeRange.ALL, 10)
	return render_template("dashboard/statistics.html", top_songs=top_songs, top_artists=top_artists)


@bp.route("/playlists/<playlist_id>", methods=("GET", "POST"))
@login_required
def playlistView(playlist_id):
	playlist_details = spotifyAPI.get_playlist_details(playlist_id)
	playlist_tracks = spotifyAPI.get_playlist_tracks(playlist_id)
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	for index, track in enumerate(playlist_tracks):
		milliseconds = track["track"]["duration_ms"]
		minutes = milliseconds // 60000
		seconds = (milliseconds // 1000) % 60
		playlist_tracks[index]["track"]["length"] = {"minutes": minutes, "seconds": seconds}
		playlist_tracks[index]["track"]["album"]["release_date"] = track["track"]["album"]["release_date"][:4]
		timestamp = track["added_at"]
		date = (timestamp[:10]).split("-")
		playlist_tracks[index]["date_added"] = {"day": date[2], "month": date[1], "month_name": months[int(date[1])-1], "year": date[0]}
	return render_template("dashboard/playlistView.html", playlist_name=playlist_details["name"], tracks=playlist_tracks)
