drop table if exists static_clues;
create table static_clues (
    id integer primary key autoincrement,
    secret_object_id integer not null,
    secret_object_name text not null,
    clue_object text not null,
    attribute text not null,
    clue_order integer not null
);

insert into static_clues (secret_object_id, secret_object_name, clue_object, attribute, clue_order) values
    (1, 'huckleberry', 'baseball', 'shape', 1),
    (1, 'huckleberry', 'dime', 'size', 2),
    (1, 'huckleberry', 'banana', 'category', 3),
    (1, 'huckleberry', 'sky', 'color', 4);

