# huckleberry

## Game Rules

Huckleberry is a game where one player (the clue giver) has a secret object and other players (the guessers) try to guess what that secret object is.

The game begins when the clue giver shares the first clue object. A clue object must share at least one attribute with the secret object. The four possible attributes are shape, size, color, and category. For example, if the secret object is a huckleberry, the clue object could be a baseball, since a baseball and a huckleberry are the same shape (i.e. a sphere). However, the clue giver does not tell the guessers what attribute is common between the clue object and the secret object. So, from the perspective of the guessers, a clue of "baseball" could mean that the object is white (i.e. shares the color attribute), is a sports object (i.e. shares the category attribute), or is a potato (i.e. shares the size attribute).

After the first clue, the guessers can submit guesses about what they think the secret object might be. For example, if the clue was baseball, a guesser might say, "I think the secret object is snow, since both are white".

Once all of the guessers have gone, the clue giver shares a second clue. This clue object must also share at least one attribute with the secret object. And it must be a different attribute than the first clue. Continuing our example, the second clue could be "the sky", since the sky and a baseball are both blue. At this point, guessers are thinking that the secret object could be a white object that is the size of the sky, a sports object that is blue, or any other combination of these two clues.

After each new clue, players can try to guess what the secret object is. Once four clue objects have been given (each clue object must share a different attribute with the secret object), players can ask the clue giver to tell them what attribute a clue object shares with the secret object.

### Spirit of the Game

This game is fun to play with friends, but it shouldn't be taken too competitively. The point of the game is to be creative with your clues and guesses. There is a lot of subjectivity around these clues. For example, how do we determine if a potato and a baseball are the same size or different sizes? Should baseball fall into the category of sports equipment or baseball equipment or children's toys? Some objects have very weird shapes, colors, sizes, and categories, which makes it difficult to find a clue object that shares the attribute. You can stretch the boundaries of what attributes match, as long as the spirit of your decision is to promote creativity and fun.

## Ways to Play

There are three ways to play.

1. A human gives clues, humans guess objects.
2. A computer gives clues, humans guess objects.
3. A human gives clues, a computer guesses objects.

## Developer Guide

Initialize the database: `flask --app huckleberry init-db-sqlite` or `flask --app huckleberry init-db-postgresql`

Run the app in debug mode: `flask --app huckleberry run --debug`

Run the tests: `pytest`

Measure code coverage: `coverage run -m pytest`