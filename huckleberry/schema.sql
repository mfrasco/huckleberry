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
    (2, 'pencil', 'pool noodle', 'shape', 4),
    (3, 'the sun', 'the moon', 'size', 1),
    (3, 'the sun', 'golf ball', 'shape', 2),
    (3, 'the sun', 'dandelion', 'color', 3),
    (3, 'the sun', 'a black hole', 'category', 4),
    (4, 'christmas tree', 'snowman', 'category', 1),
    (4, 'christmas tree', 'traffic cone', 'shape', 2),
    (4, 'christmas tree', 'blade of grass', 'color', 3),
    (4, 'christmas tree', 'ladder', 'size', 4),
    (5, 'the white house', 'bird house', 'category', 1),
    (5, 'the white house', 'gingerbread house', 'shape', 2),
    (5, 'the white house', 'marshmallow', 'color', 3),
    (5, 'the white house', 'football field', 'size', 4);