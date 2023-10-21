from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

from PlaylistManager.db import get_db

from .auth import login_required

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/')
@login_required
def account():
	return render_template("account/account.html")

@bp.route('/changeUsername', methods=('GET', 'POST'))
@login_required
def changeUsername():
	if request.method == 'POST':
		new_username = request.form['new-username']
		db = get_db()
		error = None

		user_id = session.get('user_id')
		old_username = db.execute('SELECT username FROM user WHERE id = ?', (user_id,)).fetchone()[0]

		num_users_with_name = db.execute('SELECT COUNT(*) FROM user WHERE username = ?', (new_username)).fetchone()[0]
		if not new_username:
			error = 'Please enter a username'
		elif old_username == new_username:
			error = 'Username must not be previous username'
		elif num_users_with_name != 0:
			error = 'Username already exists'

		if error is None:
			try:
				db.execute('UPDATE user SET username = ? WHERE id = ?', (new_username, user_id))
				db.commit()
			except db.IntegrityError:
				error = 'Error occurred'
			else:
				return redirect(url_for("account.account"))

		flash(error)

	return render_template("account/changeUsername.html")

@bp.route('/changePassword', methods=('GET', 'POST'))
@login_required
def changePassword():
	return render_template("account/changePassword.html")