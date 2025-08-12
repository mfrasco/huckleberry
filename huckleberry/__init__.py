"""Initialize flask app."""
import os

from flask import Flask, render_template, session


def create_app(test_config=None):
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Default to local PostgreSQL for development
        database_url = 'postgresql://localhost/huckleberry'
    elif database_url.startswith('postgres://'):
        # Fix for Render's URL format
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=database_url,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def show_welcome():
        """Show the welcome page."""
        return render_template("welcome.html")

    from . import db

    db.init_app(app)

    # from . import auth

    # app.register_blueprint(auth.bp)

    from . import game

    app.register_blueprint(game.bp)

    return app
