import sqlite3
import json

# Charger le schéma JSON
schema_json = """{"$schema": "https://json-schema.org/draft/2020-12/schema", "items": {"properties": {"all_parts": {"items": {"properties": {"component": {"type": "string"}, "id": {"type": "string"}, "name": {"type": "string"}, "object": {"type": "string"}, "type_line": {"type": "string"}, "uri": {"type": "string"}}, "required": ["component", "id", "name", "object", "type_line", "uri"], "type": "object"}, "type": "array"}, "artist": {"type": "string"}, "artist_ids": {"items": {"type": "string"}, "type": "array"}, "booster": {"type": "boolean"}, "border_color": {"type": "string"}, "card_back_id": {"type": "string"}, "card_faces": {"items": {"properties": {"artist": {"type": "string"}, "artist_id": {"type": "string"}, "color_indicator": {"items": {"type": "string"}, "type": "array"}, "colors": {"items": {"type": "string"}, "type": "array"}, "flavor_name": {"type": "string"}, "flavor_text": {"type": "string"}, "illustration_id": {"type": "string"}, "image_uris": {"properties": {"art_crop": {"type": "string"}, "border_crop": {"type": "string"}, "large": {"type": "string"}, "normal": {"type": "string"}, "png": {"type": "string"}, "small": {"type": "string"}}, "required": ["art_crop", "border_crop", "large", "normal", "png", "small"], "type": "object"}, "loyalty": {"type": "string"}, "mana_cost": {"type": "string"}, "name": {"type": "string"}, "object": {"type": "string"}, "oracle_text": {"type": "string"}, "power": {"type": "string"}, "printed_name": {"type": "string"}, "printed_text": {"type": "string"}, "printed_type_line": {"type": "string"}, "toughness": {"type": "string"}, "type_line": {"type": "string"}, "watermark": {"type": "string"}}, "required": ["artist", "artist_id", "mana_cost", "name", "object", "oracle_text", "type_line"], "type": "object"}, "type": "array"}, "cardmarket_id": {"type": "integer"}, "cmc": {"type": "number"}, "collector_number": {"type": "string"}, "color_identity": {"items": {"type": "string"}, "type": "array"}, "color_indicator": {"items": {"type": "string"}, "type": "array"}, "colors": {"items": {"type": "string"}, "type": "array"}, "content_warning": {"type": "boolean"}, "digital": {"type": "boolean"}, "edhrec_rank": {"type": "integer"}, "finishes": {"items": {"type": "string"}, "type": "array"}, "flavor_text": {"type": "string"}, "foil": {"type": "boolean"}, "frame": {"type": "string"}, "frame_effects": {"items": {"type": "string"}, "type": "array"}, "full_art": {"type": "boolean"}, "games": {"items": {"type": "string"}, "type": "array"}, "highres_image": {"type": "boolean"}, "id": {"type": "string"}, "illustration_id": {"type": "string"}, "image_status": {"type": "string"}, "image_uris": {"properties": {"art_crop": {"type": "string"}, "border_crop": {"type": "string"}, "large": {"type": "string"}, "normal": {"type": "string"}, "png": {"type": "string"}, "small": {"type": "string"}}, "required": ["art_crop", "border_crop", "large", "normal", "png", "small"], "type": "object"}, "keywords": {"items": {"type": "string"}, "type": "array"}, "lang": {"type": "string"}, "layout": {"type": "string"}, "legalities": {"properties": {"alchemy": {"type": "string"}, "brawl": {"type": "string"}, "commander": {"type": "string"}, "duel": {"type": "string"}, "explorer": {"type": "string"}, "future": {"type": "string"}, "gladiator": {"type": "string"}, "historic": {"type": "string"}, "historicbrawl": {"type": "string"}, "legacy": {"type": "string"}, "modern": {"type": "string"}, "oathbreaker": {"type": "string"}, "oldschool": {"type": "string"}, "pauper": {"type": "string"}, "paupercommander": {"type": "string"}, "penny": {"type": "string"}, "pioneer": {"type": "string"}, "predh": {"type": "string"}, "premodern": {"type": "string"}, "standard": {"type": "string"}, "vintage": {"type": "string"}}, "required": ["alchemy", "brawl", "commander", "duel", "explorer", "future", "gladiator", "historic", "historicbrawl", "legacy", "modern", "oathbreaker", "oldschool", "pauper", "paupercommander", "penny", "pioneer", "predh", "premodern", "standard", "vintage"], "type": "object"}, "loyalty": {"type": "string"}, "mana_cost": {"type": "string"}, "multiverse_ids": {"items": {"type": "integer"}, "type": "array"}, "name": {"type": "string"}, "nonfoil": {"type": "boolean"}, "object": {"type": "string"}, "oracle_id": {"type": "string"}, "oracle_text": {"type": "string"}, "oversized": {"type": "boolean"}, "penny_rank": {"type": "integer"}, "power": {"type": "string"}, "prices": {"properties": {"eur": {"type": ["null", "string"]}, "eur_foil": {"type": ["null", "string"]}, "tix": {"type": "null"}, "usd": {"type": ["null", "string"]}, "usd_etched": {"type": "null"}, "usd_foil": {"type": ["null", "string"]}}, "required": ["eur", "eur_foil", "tix", "usd", "usd_etched", "usd_foil"], "type": "object"}, "printed_name": {"type": "string"}, "printed_text": {"type": "string"}, "printed_type_line": {"type": "string"}, "prints_search_uri": {"type": "string"}, "produced_mana": {"items": {"type": "string"}, "type": "array"}, "promo": {"type": "boolean"}, "promo_types": {"items": {"type": "string"}, "type": "array"}, "rarity": {"type": "string"}, "related_uris": {"properties": {"edhrec": {"type": "string"}, "gatherer": {"type": "string"}, "tcgplayer_infinite_articles": {"type": "string"}, "tcgplayer_infinite_decks": {"type": "string"}}, "required": [], "type": "object"}, "released_at": {"type": "string"}, "reprint": {"type": "boolean"}, "reserved": {"type": "boolean"}, "rulings_uri": {"type": "string"}, "scryfall_set_uri": {"type": "string"}, "scryfall_uri": {"type": "string"}, "security_stamp": {"type": "string"}, "set": {"type": "string"}, "set_id": {"type": "string"}, "set_name": {"type": "string"}, "set_search_uri": {"type": "string"}, "set_type": {"type": "string"}, "set_uri": {"type": "string"}, "story_spotlight": {"type": "boolean"}, "tcgplayer_id": {"type": "integer"}, "textless": {"type": "boolean"}, "toughness": {"type": "string"}, "type_line": {"type": "string"}, "uri": {"type": "string"}, "variation": {"type": "boolean"}, "variation_of": {"type": "string"}, "watermark": {"type": "string"}}, "required": ["artist", "artist_ids", "booster", "border_color", "cmc", "collector_number", "color_identity", "digital", "finishes", "foil", "frame", "full_art", "games", "highres_image", "id", "image_status", "keywords", "lang", "layout", "legalities", "multiverse_ids", "name", "nonfoil", "object", "oracle_id", "oversized", "prices", "prints_search_uri", "promo", "rarity", "related_uris", "released_at", "reprint", "reserved", "rulings_uri", "scryfall_set_uri", "scryfall_uri", "set", "set_id", "set_name", "set_search_uri", "set_type", "set_uri", "story_spotlight", "textless", "type_line", "uri", "variation"], "type": "object"}, "type": "array"}"""  # Insérez votre schéma JSON ici
schema = json.loads(schema_json)

# Créer la base de données SQLite
conn = sqlite3.connect("cartes_magic.db")
cursor = conn.cursor()

# Créer les tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY,
    artist TEXT,
    booster BOOLEAN,
    border_color TEXT,
    card_back_id TEXT,
    cardmarket_id INTEGER,
    cmc REAL,
    collector_number TEXT,
    digital BOOLEAN,
    edhrec_rank INTEGER,
    finishes TEXT,
    flavor_text TEXT,
    foil BOOLEAN,
    frame TEXT,
    full_art BOOLEAN,
    games TEXT,
    highres_image BOOLEAN,
    illustration_id TEXT,
    image_status TEXT,
    lang TEXT,
    layout TEXT,
    legalities TEXT,
    loyalty TEXT,
    mana_cost TEXT,
    multiverse_ids TEXT,
    name TEXT,
    nonfoil BOOLEAN,
    object TEXT,
    oracle_id TEXT,
    oracle_text TEXT,
    oversized BOOLEAN,
    penny_rank INTEGER,
    power TEXT,
    prices TEXT,
    printed_name TEXT,
    printed_text TEXT,
    printed_type_line TEXT,
    prints_search_uri TEXT,
    produced_mana TEXT,
    promo BOOLEAN,
    promo_types TEXT,
    rarity TEXT,
    related_uris TEXT,
    released_at TEXT,
    reprint BOOLEAN,
    reserved BOOLEAN,
    rulings_uri TEXT,
    scryfall_set_uri TEXT,
    scryfall_uri TEXT,
    security_stamp TEXT,
    _set TEXT,
    set_id TEXT,
    set_name TEXT,
    set_search_uri TEXT,
    set_type TEXT,
    set_uri TEXT,
    story_spotlight BOOLEAN,
    tcgplayer_id INTEGER,
    textless BOOLEAN,
    toughness TEXT,
    type_line TEXT,
    uri TEXT,
    variation BOOLEAN,
    variation_of TEXT,
    watermark TEXT
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS artist_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    artist_id TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS color_identity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    color TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS color_indicator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    color TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS colors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    color TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS card_faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    artist TEXT,
    artist_id TEXT,
    color_indicator TEXT,
    colors TEXT,
    flavor_name TEXT,
    flavor_text TEXT,
    illustration_id TEXT,
    image_uris TEXT,
    loyalty TEXT,
    mana_cost TEXT,
    name TEXT,
    object TEXT,
    oracle_text TEXT,
    power TEXT,
    printed_name TEXT,
    printed_text TEXT,
    printed_type_line TEXT,
    toughness TEXT,
    type_line TEXT,
    watermark TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)""")

# Créer la table 'card_faces_image_uris'
cursor.execute("""
CREATE TABLE IF NOT EXISTS card_faces_image_uris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_faces_id INTEGER,
    art_crop TEXT,
    border_crop TEXT,
    large TEXT,
    normal TEXT,
    png TEXT,
    small TEXT,
    FOREIGN KEY (card_faces_id) REFERENCES card_faces (id)
)
""")

# Créer la table 'legalities'
cursor.execute("""
CREATE TABLE IF NOT EXISTS legalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    alchemy TEXT,
    brawl TEXT,
    commander TEXT,
    duel TEXT,
    explorer TEXT,
    future TEXT,
    gladiator TEXT,
    historic TEXT,
    historicbrawl TEXT,
    legacy TEXT,
    modern TEXT,
    oathbreaker TEXT,
    oldschool TEXT,
    pauper TEXT,
    paupercommander TEXT,
    penny TEXT,
    pioneer TEXT,
    predh TEXT,
    premodern TEXT,
    standard TEXT,
    vintage TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
""")

# Créer la table 'prices'
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    eur TEXT,
    eur_foil TEXT,
    tix TEXT,
    usd TEXT,
    usd_etched TEXT,
    usd_foil TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
""")

# Créer la table 'related_uris'
cursor.execute("""
CREATE TABLE IF NOT EXISTS related_uris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    edhrec TEXT,
    gatherer TEXT,
    tcgplayer_infinite_articles TEXT,
    tcgplayer_infinite_decks TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS finishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    finish TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS frame_effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    frame_effect TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    game TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    keyword TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS produced_mana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    mana TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promo_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT,
    promo_type TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
""")

# Valider les modifications et fermer la connexion
conn.commit()
conn.close()
