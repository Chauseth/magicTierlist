import mysql.connector
import json
import traceback
import os

config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'raise_on_warnings': True
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def import_cards():
    with open("cartes_magic.json", "r", encoding="utf-8") as f:
        cards_data = json.load(f)

    # Parcourir chaque carte dans le fichier JSON
    for card in cards_data:

        card["printed_name"] = card.get("printed_name", "")
        card["printed_type_line"] = card.get("printed_type_line", "")
        card["printed_text"] = card.get("printed_text", "")

        cursor.execute('SELECT id FROM sets WHERE scryfall_id = %s',
                       (card["set_id"],))
        set_id_result = cursor.fetchone()
        if set_id_result:
            card["set_id"] = set_id_result[0]
        else:
            print(f"Pas de set  trouvé pour ce scryfall_id: {card['set_id']}")
            continue

        if "image_uris" in card:
            card["img_small"] = card["image_uris"].get("small", "")
            card["img_normal"] = card["image_uris"].get("normal", "")
            card["img_large"] = card["image_uris"].get("large", "")
            card["img_png"] = card["image_uris"].get("png", "")
            card["img_art_crop"] = card["image_uris"].get("art_crop", "")
            card["img_border_crop"] = card["image_uris"].get("border_crop", "")
        else:
            card["img_small"] = card["card_faces"][0].get("small", "")
            card["img_normal"] = card["card_faces"][0].get("normal", "")
            card["img_large"] = card["card_faces"][0].get("large", "")
            card["img_png"] = card["card_faces"][0].get("png", "")
            card["img_art_crop"] = card["card_faces"][0].get("art_crop", "")
            card["img_border_crop"] = card["card_faces"][0].get("border_crop", "")

        if "card_faces" in card:
            card[
                "printed_name"] = f'{card["card_faces"][0].get("printed_name", "name")} | {card["card_faces"][1].get("printed_name", "name")}'
            card[
                "printed_type_line"] = f'{card["card_faces"][0].get("printed_type_line", "type_line")} | {card["card_faces"][1].get("printed_type_line", "type_line")}'
            card[
                "printed_text"] = f'{card["card_faces"][0].get("printed_text", "oracle_text")} | {card["card_faces"][1].get("printed_text", "oracle_text")}'
            card[
                "oracle_text"] = f'{card["card_faces"][0].get("oracle_text", "")} | {card["card_faces"][1].get("oracle_text", "")}'

        if card["printed_name"] == "" or card["printed_type_line"] == "" or card["printed_text"] == "":
            continue

        if "gatherer" in card["related_uris"]:
            card["gatherer"] = card["related_uris"]["gatherer"]
        else:
            card["gatherer"] = None

        if "loyalty" not in card:
            card["loyalty"] = None

        if "produced_mana" not in card:
            card["produced_mana"] = None
        else:
            card["produced_mana"] = ",".join(card["produced_mana"])

        if "mana_cost" not in card:
            card["mana_cost"] = None

        if "power" not in card:
            card["power"] = None

        if "toughness" not in card:
            card["toughness"] = None

        try:
            cursor.execute("""
                INSERT INTO cards (scryfall_id, oracle_id, name, printed_name, lang, released_at, scryfall_uri, mana_cost, cmc, type_line, printed_type_line, oracle_text, printed_text, power, toughness, set_id, `number`, rarity, gatherer_url, loyalty, produced_mana)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                card["id"], card["oracle_id"], card["name"], card["printed_name"], card["lang"], card["released_at"],
                card["scryfall_uri"], card["mana_cost"], card["cmc"], card["type_line"], card["printed_type_line"],
                card["oracle_text"], card["printed_text"], card["power"], card["toughness"], card["set_id"],
                card["collector_number"], card["rarity"], card["gatherer"], card["loyalty"], card["produced_mana"]))

            cursor.execute(
                "INSERT INTO image_uris (scryfall_id, small, normal, large, png, art_crop, border_crop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (card["id"], card["img_small"], card["img_normal"], card["img_large"], card["img_png"],
                 card["img_art_crop"], card["img_border_crop"]))

        except Exception as e:
            traceback.print_exc()
            print(card)
            exit()


def import_sets():
    with open("sets.json", "r", encoding="utf-8") as f:
        sets_data = json.load(f)

    for set in sets_data:
        cursor.execute(
            "INSERT INTO sets (code, name, icon_svg_uri, scryfall_id, released_at, scryfall_uri, set_type) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (set["code"], set["name"], set["icon_svg_uri"], set["id"], set["released_at"], set["scryfall_uri"],
             set["set_type"]))


# import_sets()
import_cards()

# Valider les modifications et fermer la connexion
conn.commit()
conn.close()
