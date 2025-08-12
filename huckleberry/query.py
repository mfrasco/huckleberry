"""Helper functions for executing queries."""

import psycopg2.extras
from huckleberry.db import get_db


def fetch_one(query, args=None):
    """Execute a query where we are intending to get a single value."""
    if args is None:
        args = []
    
    db = get_db()
    
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


def fetch_all(query, args=None):
    """Execute a query where we are intending to get multiple values."""
    if args is None:
        args = []
    
    db = get_db()
    
    # PostgreSQL uses %s for placeholders
    query = query.replace('?', '%s')
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, args)
    result = cur.fetchall()
    cur.close()
    
    # Return as list of dictionaries
    return result if result else []


def execute(query, args=None, commit=True):
    """Execute a query where we are intending to write results to the database."""
    if args is None:
        args = []
    
    db = get_db()
    
    # PostgreSQL uses %s for placeholders
    query = query.replace('?', '%s')
    cur = db.cursor()
    cur.execute(query, args)
    if commit:
        db.commit()
    cur.close()
