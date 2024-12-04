"""Module for the game."""
import random

from flask import Blueprint, render_template

from huckleberry.query import fetch_all, fetch_one

bp = Blueprint("game", __name__)

def get_random_object_id():
    """Query id for a random object."""
    query = """
        select max(secret_object_id) as num_secret_objects
        from static_clues
    """
    num_secret_objects = fetch_one(query)
    return random.randint(1, num_secret_objects)


def get_object_clues(secret_object_id):
    """Query static clues for a specific object."""
    query = """
        select
            secret_object_name
            , clue_object
            , attribute
        from static_clues
        where secret_object_id = ?
        order by clue_order
    """
    return fetch_all(query, args=[secret_object_id])


@bp.route("/play")
def show_play_with_computer():
    """Show the page to play with computer."""
    secret_object_id = get_random_object_id()
    clues = get_object_clues(secret_object_id=secret_object_id)
    return render_template("play_with_computer.html", clues=clues)