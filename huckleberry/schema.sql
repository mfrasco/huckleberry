drop table if exists secret_objects;
create table secret_objects (
    id integer primary key autoincrement,
    secret_object text not null
);

drop table if exists clues;
create table clues (
    id integer primary key autoincrement,
    secret_object_id integer not null,
    clue_object text not null,
    attribute integer not null,
    clue_order integer not null
);