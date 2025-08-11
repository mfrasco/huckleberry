"""Module for the game."""
import random

from flask import Blueprint, render_template, session, request, redirect, url_for

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


def is_correct_guess(guess, secret_object_name):
    """Check if guess matches secret object (case-insensitive)."""
    return guess.lower().strip() == secret_object_name.lower().strip()


def start_new_game():
    """Initialize a new game session."""
    secret_object_id = get_random_object_id()
    clues_data = get_object_clues(secret_object_id=secret_object_id)
    
    # Convert Row objects to clue structure
    clues = []
    for idx, clue in enumerate(clues_data):
        clues.append({
            'object_name': clue['clue_object'],
            'clue_number': idx + 1,
            'is_attribute_revealed': False,
            'attribute': clue['attribute']
        })
    
    session['game_state'] = {
        'secret_object_id': secret_object_id,
        'secret_object_name': clues_data[0]['secret_object_name'],
        'clues': clues,
        'current_clue_number': 0,
        'previous_guesses': [],
        'game_over': False,
        'won': False,
        'show_guess_feedback': False
    }


@bp.route("/play")
def show_computer_gives_clues_human_guesses():
    """Show the page to play with computer."""
    if 'game_state' not in session:
        start_new_game()
    
    game_state = session['game_state']
    
    if game_state['game_over']:
        return render_template(
            "computer_gives_clues_human_guesses.html",
            game_over=True,
            won=game_state['won'],
            secret_object_name=game_state['secret_object_name'],
            clues=game_state['clues']
        )
    
    current_clue_idx = game_state['current_clue_number']
    
    if current_clue_idx < 4:
        # For clues 1-4, we are getting the name of the clue object
        current_clue_object = game_state['clues'][current_clue_idx]['object_name']
        current_clue_attribute = None
    else:
        # For clues 5-8, we're revealing attributes of the selected_object
        current_clue_object = game_state['selected_object']
        for clue in game_state['clues']:
            if current_clue_object == clue['object_name']:
                current_clue_attribute = clue['attribute']
    
    # Generate feedback message if needed
    guess_feedback = None
    if game_state.get('show_guess_feedback', False) and game_state['previous_guesses']:
        last_guess = game_state['previous_guesses'][-1]
        # This can be enhanced later with more intelligent responses
        guess_feedback = f"No, the secret object isn't {last_guess}."
    
    return render_template(
        "computer_gives_clues_human_guesses.html",
        game_over=False,
        current_clue_object=current_clue_object,
        current_clue_attribute=current_clue_attribute,
        current_clue_number=current_clue_idx + 1,
        secret_object_id=game_state['secret_object_id'],
        previous_guesses=game_state['previous_guesses'],
        clues=game_state['clues'],
        guess_feedback=guess_feedback
    )


@bp.route("/submit_guess", methods=["POST"])
def submit_guess():
    """Handle guess submission - only check guess and add to history."""
    if 'game_state' not in session:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    guess = request.form.get('guess', '').strip()
    if not guess:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    game_state = session['game_state']
    
    if guess not in game_state['previous_guesses']:
        game_state['previous_guesses'].append(guess)
    
    if is_correct_guess(guess, game_state['secret_object_name']):
        game_state['game_over'] = True
        game_state['won'] = True
        game_state['show_guess_feedback'] = False
    else:
        # Show feedback for incorrect guess
        game_state['show_guess_feedback'] = True
    
    session['game_state'] = game_state
    return redirect(url_for('game.show_computer_gives_clues_human_guesses'))


@bp.route("/next_clue", methods=["POST"])
def next_clue():
    """Advance to the next clue."""
    if 'game_state' not in session:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    game_state = session['game_state']
    game_state['current_clue_number'] += 1
    # Clear feedback when moving to next clue
    game_state['show_guess_feedback'] = False

    session['game_state'] = game_state
    return redirect(url_for('game.show_computer_gives_clues_human_guesses'))


@bp.route("/reveal_attribute", methods=["POST"])
def reveal_attribute():
    """Reveal the attribute of a selected clue object."""
    if 'game_state' not in session:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    clue_object = request.form.get('clue_object', '').strip()
    if not clue_object:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    game_state = session['game_state']
    game_state['selected_object'] = clue_object
    
    # Find the clue and mark its attribute as revealed
    for clue in game_state['clues']:
        if clue['object_name'] == clue_object:
            clue['is_attribute_revealed'] = True
            game_state['current_clue_number'] += 1
            break
    
    session['game_state'] = game_state
    return redirect(url_for('game.show_computer_gives_clues_human_guesses'))


@bp.route("/end_game", methods=["POST"])
def end_game():
    """End the current game when player gives up."""
    if 'game_state' not in session:
        return redirect(url_for('game.show_computer_gives_clues_human_guesses'))
    
    game_state = session['game_state']
    game_state['game_over'] = True
    game_state['won'] = False
    
    session['game_state'] = game_state
    return redirect(url_for('game.show_computer_gives_clues_human_guesses'))


@bp.route("/new_game")
def new_game():
    """Start a new game by clearing session."""
    session.pop('game_state', None)
    return redirect(url_for('game.show_computer_gives_clues_human_guesses'))