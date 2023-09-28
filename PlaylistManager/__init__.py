import os, secrets
from flask import Flask, render_template


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'PlaylistManager.sqlite'),
	)
	app.secret_key = secrets.token_hex(16)
	app.config['SESSION_COOKIE_SECURE'] = True
	app.config['SESSION_COOKIE_HTTPONLY'] = True
	app.config['PERMANENT_SESSION_LIFETIME'] = 7200

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/')
	def index():
		return render_template('index.html')
	
	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import dashboard
	app.register_blueprint(dashboard.bp)

	from . import account
	app.register_blueprint(account.bp)

	return app