from flask import Blueprint, render_template

from PlaylistManager.db import get_db

from .auth import login_required

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def account():
	return render_template("account/account.html")