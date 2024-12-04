"""Helper functions for executing queries."""

from huckleberry.db import get_db


def fetch_one(query, args=None):
    """Execute a query where we are intending to get a single value."""
    if args is None:
        args = []
    cur = get_db().execute(query, args)
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
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    return result


def execute(query, args=None, commit=True):
    """Execute a query where we are intending to write results to the database."""
    if args is None:
        args = []
    db = get_db()
    db.execute(query, args)
    if commit:
        db.commit()
