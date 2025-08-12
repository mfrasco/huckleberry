"""Database module."""
import sqlite3
import os

import click
from flask import current_app, g


def connect_db():
    """Connects to the specific database.
    
    This function can be used for debugging purposes,
    when you want to query the database without operating in the context of the flask app.
    """
    rv = sqlite3.connect("instance/huckleberry.sqlite")
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Get database connection."""
    if "db" not in g:
        if current_app.config.get("IS_POSTGRESQL"):
            import psycopg2
            import psycopg2.extras
            g.db = psycopg2.connect(current_app.config["DATABASE"])
            # We'll handle cursor creation when needed
        else:
            g.db = sqlite3.connect(
                current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db_postgresql():
    """Initialize database."""
    db = get_db()
    with current_app.open_resource("schema_postgresql.sql") as f:
        cursor = db.cursor()
        cursor.execute(f.read().decode("utf8"))
        db.commit()


def init_db_sqlite():
    """Initialize database."""
    db = get_db()
    with current_app.open_resource("schema_sqlite.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db-postgresql")
def init_db_postgresql_command():
    """Clear the existing data and create new tables."""
    init_db_postgresql()
    click.echo("Initialized the database.")


@click.command("init-db-sqlite")
def init_db_sqlite_command():
    """Clear the existing data and create new tables."""
    init_db_sqlite()
    click.echo("Initialized the database.")


def init_app(app):
    """Initialize the app."""
    app.teardown_appcontext(close_db)
    if app.config.get("IS_POSTGRESQL"):
        app.cli.add_command(init_db_postgresql_command)
    else:
        app.cli.add_command(init_db_sqlite_command)
