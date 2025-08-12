DROP TABLE IF EXISTS static_clues;
CREATE TABLE static_clues (
    id SERIAL PRIMARY KEY,
    secret_object_id INTEGER NOT NULL,
    secret_object_name TEXT NOT NULL,
    clue_object TEXT NOT NULL,
    attribute TEXT NOT NULL,
    clue_order INTEGER NOT NULL
);

INSERT INTO static_clues (secret_object_id, secret_object_name, clue_object, attribute, clue_order) VALUES
    (1, 'blueberry', 'baseball', 'shape', 1),
    (1, 'blueberry', 'dime', 'size', 2),
    (1, 'blueberry', 'banana', 'category', 3),
    (1, 'blueberry', 'sky', 'color', 4),
    (2, 'pencil', 'piece of paper', 'category', 1),
    (2, 'pencil', 'school bus', 'color', 2),
    (2, 'pencil', 'knife', 'size', 3),
    (2, 'pencil', 'pool noodle', 'shape', 4);