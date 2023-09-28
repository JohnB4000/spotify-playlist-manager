import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from PlaylistManager.db import get_db

from .auth import login_required

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def account():
	return render_template("account/account.html")