"""Database module."""
import os

import click
import psycopg2
import psycopg2.extras
from flask import current_app, g


def get_db():
    """Get PostgreSQL database connection."""
    if "db" not in g:
        g.db = psycopg2.connect(current_app.config["DATABASE"])
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize PostgreSQL database."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        cursor = db.cursor()
        cursor.execute(f.read().decode("utf8"))
        db.commit()
        cursor.close()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the PostgreSQL database.")


def init_app(app):
    """Initialize the app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
