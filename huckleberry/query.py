"""Helper functions for executing queries."""

from flask import current_app
from huckleberry.db import get_db


def fetch_one(query, args=None):
    """Execute a query where we are intending to get a single value."""
    if args is None:
        args = []
    
    db = get_db()
    
    if current_app.config.get("IS_POSTGRESQL"):
        import psycopg2.extras
        # PostgreSQL uses %s for placeholders
        query = query.replace('?', '%s')
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, args)
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        else:
            # PostgreSQL returns a dictionary, get first value
            return list(result.values())[0]
    else:
        # SQLite
        cur = db.execute(query, args)
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        else:
            return result[0]


def fetch_all(query, args=None):
    """Execute a query where we are intending to get multiple values."""
    if args is None:
        args = []
    
    db = get_db()
    
    if current_app.config.get("IS_POSTGRESQL"):
        import psycopg2.extras
        # PostgreSQL uses %s for placeholders
        query = query.replace('?', '%s')
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, args)
        result = cur.fetchall()
        cur.close()
        # Return as list of dictionaries for compatibility
        return result if result else []
    else:
        # SQLite
        cur = db.execute(query, args)
        result = cur.fetchall()
        cur.close()
        return result


def execute(query, args=None, commit=True):
    """Execute a query where we are intending to write results to the database."""
    if args is None:
        args = []
    
    db = get_db()
    
    if current_app.config.get("IS_POSTGRESQL"):
        # PostgreSQL uses %s for placeholders
        query = query.replace('?', '%s')
        cur = db.cursor()
        cur.execute(query, args)
        if commit:
            db.commit()
        cur.close()
    else:
        # SQLite
        db.execute(query, args)
        if commit:
            db.commit()
