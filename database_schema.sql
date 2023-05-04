CREATE TABLE sets
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    code         TEXT,
    name         TEXT,
    icon_svg_uri TEXT,
    scryfall_id  TEXT,
    released_at  TEXT,
    scryfall_uri TEXT,
    set_type     TEXT
);


CREATE TABLE cards
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    scryfall_id       TEXT UNIQUE,
    oracle_id         TEXT,
    name              TEXT,
    printed_name      TEXT,
    lang              TEXT,
    released_at       TEXT,
    scryfall_uri      TEXT,
    mana_cost         TEXT,
    cmc               TEXT,
    type_line         TEXT,
    printed_type_line TEXT,
    oracle_text       TEXT,
    printed_text      TEXT,
    power             TEXT,
    toughness        TEXT,
    set_id            INTEGER,
    number            INTEGER,
    rarity            TEXT,
    gatherer_url      TEXT,
    loyalty           INTEGER,
    produced_mana     TEXT,
    FOREIGN KEY (set_id) REFERENCES sets (id) ON DELETE CASCADE ON UPDATE CASCADE


);

CREATE TABLE image_uris
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    scryfall_id     TEXT,
    small       TEXT,
    normal      TEXT,
    large       TEXT,
    png         TEXT,
    art_crop    TEXT,
    border_crop TEXT,
    FOREIGN KEY (scryfall_id) REFERENCES cards (scryfall_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tierlists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    set_id INTEGER,
    created_at
    FOREIGN KEY (set_id) REFERENCES sets (id) ON DELETE CASCADE ON UPDATE CASCADE
)

CREATE TABLE IF NOT EXISTS card_ratings (
    id INTEGER PRIMARY KEY,
    card_id INTEGER NOT NULL,
    tierlist_id INTEGER NOT NULL,
    rating TEXT NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards (id),
    FOREIGN KEY (tierlist_id) REFERENCES tierlists (id),
    UNIQUE (card_id, tierlist_id)
);
