import mysql.connector
import json
import traceback
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

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
        try:
            if card["lang"] not in ["fr", "en"]:
                continue

            cursor.execute('SELECT id FROM sets WHERE scryfall_id = %s',
                           (card["set_id"],))
            set_id_result = cursor.fetchone()
            if set_id_result:
                card["set_id"] = set_id_result[0]
            else:
                print(f"Pas de set  trouvé pour ce scryfall_id: {card['set_id']}")
                continue

            if card.get("card_faces") is None:
                card["printed_name"] = card.get("printed_name", "")
                card["printed_type_line"] = card.get("printed_type_line", "type_line")
                card["printed_text"] = card.get("printed_text", "")
                card["img_small"] = card["image_uris"].get("small", "")
                card["img_normal"] = card["image_uris"].get("normal", "")
                card["img_large"] = card["image_uris"].get("large", "")
                card["img_png"] = card["image_uris"].get("png", "")
                card["img_art_crop"] = card["image_uris"].get("art_crop", "")
                card["img_border_crop"] = card["image_uris"].get("border_crop", "")
                card["other_face"] = None

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

            else:
                card["id_2"] = str(uuid.uuid4())

                card["other_face"] = card["id_2"]
                card["other_face_2"] = card["id"]

                card["printed_name"] = card["card_faces"][0].get("printed_name", "name")
                card["printed_name_2"] = card["card_faces"][1].get("printed_name", "name")

                card["oracle_id"] = card["card_faces"][0].get("oracle_id", None)
                card["oracle_id_2"] = card["card_faces"][1].get("oracle_id", None)

                if "mana_cost" not in card["card_faces"][0] and "mana_cost" not in card["card_faces"][1]:
                    card["mana_cost"] = None
                    card["mana_cost_2"] = None
                else:
                    card["mana_cost"] = card["card_faces"][0].get("mana_cost", None)
                    card["mana_cost_2"] = card["card_faces"][1].get("mana_cost", None)

                if "power" not in card["card_faces"][0] and "power" not in card["card_faces"][1]:
                    card["power"] = None
                    card["power_2"] = None
                else:
                    card["power"] = card["card_faces"][0].get("power", None)
                    card["power_2"] = card["card_faces"][1].get("power", None)

                if "toughness" not in card["card_faces"][0] and "toughness" not in card["card_faces"][1]:
                    card["toughness"] = None
                    card["toughness_2"] = None
                else:
                    card["toughness"] = card["card_faces"][0].get("toughness", None)
                    card["toughness_2"] = card["card_faces"][1].get("toughness", None)

                if "loyalty" not in card["card_faces"][0] and "loyalty" not in card["card_faces"][1]:
                    card["loyalty"] = None
                    card["loyalty_2"] = None
                else:
                    card["loyalty"] = card["card_faces"][0].get("loyalty", None)
                    card["loyalty_2"] = card["card_faces"][1].get("loyalty", None)

                card["printed_text"] = card["card_faces"][0].get("printed_text", "oracle_text")
                card["printed_text_2"] = card["card_faces"][1].get("printed_text", "oracle_text")

                card["oracle_text"] = card["card_faces"][0].get("oracle_text", None)
                card["oracle_text_2"] = card["card_faces"][1].get("oracle_text", None)

                if "produced_mana" not in card["card_faces"][0] and "produced_mana" not in card["card_faces"][1]:
                    card["produced_mana"] = None
                    card["produced_mana_2"] = None
                else:
                    card["produced_mana"] = card["card_faces"][0].get("produced_mana", None)
                    card["produced_mana_2"] = card["card_faces"][1].get("produced_mana", None)

                if "cmc" not in card["card_faces"][0] and "cmc" not in card["card_faces"][1]:
                    if "cmc" not in card:
                        card["cmc"] = None
                        card["cmc_2"] = None
                    else:
                        card["cmc_2"] = card["cmc"]
                else:
                    card["cmc"] = card["card_faces"][0].get("cmc", None)
                    card["cmc_2"] = card["card_faces"][1].get("cmc", None)

                if "printed_type_line" not in card["card_faces"][0] and "printed_type_line" not in card["card_faces"][1]:
                    if "type_line" not in card["card_faces"][0] and "type_line" not in card["card_faces"][1]:
                        card["printed_type_line"] = None
                        card["printed_type_line_2"] = None

                        card["type_line"] = None
                        card["type_line_2"] = None
                    else:
                        card["printed_type_line"] = card.get("printed_type_line", "type_line")
                        card["printed_type_line_2"] = card.get("printed_type_line", "type_line")

                        card["type_line"] = card["card_faces"][0].get("type_line", None)
                        card["type_line_2"] = card["card_faces"][1].get("type_line", None)

                else:
                    card["printed_type_line"] = card["card_faces"][0].get("printed_type_line", "type_line")
                    card["printed_type_line_2"] = card["card_faces"][1].get("printed_type_line", "type_line")

                    card["type_line"] = card["card_faces"][0].get("type_line", "printed_type_line")
                    card["type_line_2"] = card["card_faces"][1].get("type_line", "printed_type_line")

                if "image_uris" not in card["card_faces"][0] and "image_uris" not in card["card_faces"][1]:
                    if "image_uris" in card:

                        card["img_small"] = card["image_uris"].get("small", "")
                        card["img_normal"] = card["image_uris"].get("normal", "")
                        card["img_large"] = card["image_uris"].get("large", "")
                        card["img_png"] = card["image_uris"].get("png", "")
                        card["img_art_crop"] = card["image_uris"].get("art_crop", "")
                        card["img_border_crop"] = card["image_uris"].get("border_crop", "")

                        card["img_small_2"] = card["image_uris"].get("small", "")
                        card["img_normal_2"] = card["image_uris"].get("normal", "")
                        card["img_large_2"] = card["image_uris"].get("large", "")
                        card["img_png_2"] = card["image_uris"].get("png", "")
                        card["img_art_crop_2"] = card["image_uris"].get("art_crop", "")
                        card["img_border_crop_2"] = card["image_uris"].get("border_crop", "")
                    else:
                        card["img_small"] = None
                        card["img_normal"] = None
                        card["img_large"] = None
                        card["img_png"] = None
                        card["img_art_crop"] = None
                        card["img_border_crop"] = None

                        card["img_small_2"] = None
                        card["img_normal_2"] = None
                        card["img_large_2"] = None
                        card["img_png_2"] = None
                        card["img_art_crop_2"] = None
                        card["img_border_crop_2"] = None
                else:

                    card["img_small"] = card["card_faces"][0]["image_uris"].get("small", None)
                    card["img_normal"] = card["card_faces"][0]["image_uris"].get("normal", None)
                    card["img_large"] = card["card_faces"][0]["image_uris"].get("large", None)
                    card["img_png"] = card["card_faces"][0]["image_uris"].get("png", None)
                    card["img_art_crop"] = card["card_faces"][0]["image_uris"].get("art_crop", None)
                    card["img_border_crop"] = card["card_faces"][0]["image_uris"].get("border_crop", None)

                    card["img_small_2"] = card["card_faces"][1]["image_uris"].get("small", None)
                    card["img_normal_2"] = card["card_faces"][1]["image_uris"].get("normal", None)
                    card["img_large_2"] = card["card_faces"][1]["image_uris"].get("large", None)
                    card["img_png_2"] = card["card_faces"][1]["image_uris"].get("png", None)
                    card["img_art_crop_2"] = card["card_faces"][1]["image_uris"].get("art_crop", None)
                    card["img_border_crop_2"] = card["card_faces"][1]["image_uris"].get("border_crop", None)

            if card["printed_name"] == "" or card["printed_type_line"] == "" or card["printed_text"] == "":
                continue

            if "gatherer" in card["related_uris"]:
                card["gatherer"] = card["related_uris"]["gatherer"]
            else:
                card["gatherer"] = None

            if "collector_number" in card:
                card["collector_number"] = ''.join(char for char in card["collector_number"] if char.isdigit())

            if card.get("card_faces") is None:
                cursor.execute("""
                    INSERT INTO cards (scryfall_id, oracle_id, name, printed_name, lang, released_at, scryfall_uri, mana_cost, cmc, type_line, printed_type_line, oracle_text, printed_text, power, toughness, set_id, `number`, rarity, gatherer_url, loyalty, produced_mana, other_face)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                    card["id"], card["oracle_id"], card["name"], card["printed_name"], card["lang"],
                    card["released_at"],
                    card["scryfall_uri"], card["mana_cost"], card["cmc"], card["type_line"], card["printed_type_line"],
                    card["oracle_text"], card["printed_text"], card["power"], card["toughness"], card["set_id"],
                    card["collector_number"], card["rarity"], card["gatherer"], card["loyalty"], card["produced_mana"],
                    card["other_face"]))

                cursor.execute(
                    "INSERT INTO image_uris (scryfall_id, small, normal, large, png, art_crop, border_crop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (card["id"], card["img_small"], card["img_normal"], card["img_large"], card["img_png"],
                     card["img_art_crop"], card["img_border_crop"]))
            else:
                cursor.execute("""
                    INSERT INTO cards (scryfall_id, oracle_id, name, printed_name, lang, released_at, scryfall_uri, mana_cost, cmc, type_line, printed_type_line, oracle_text, printed_text, power, toughness, set_id, `number`, rarity, gatherer_url, loyalty, produced_mana, other_face)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                    card["id"], card["oracle_id"], card["name"], card["printed_name"], card["lang"],
                    card["released_at"],
                    card["scryfall_uri"], card["mana_cost"], card["cmc"], card["type_line"], card["printed_type_line"],
                    card["oracle_text"], card["printed_text"], card["power"], card["toughness"], card["set_id"],
                    card["collector_number"], card["rarity"], card["gatherer"], card["loyalty"], card["produced_mana"],
                    card["other_face"]))

                cursor.execute(
                    "INSERT INTO image_uris (scryfall_id, small, normal, large, png, art_crop, border_crop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (card["id"], card["img_small"], card["img_normal"], card["img_large"], card["img_png"],
                     card["img_art_crop"], card["img_border_crop"]))

                cursor.execute("""
                    INSERT INTO cards (scryfall_id, oracle_id, name, printed_name, lang, released_at, scryfall_uri, mana_cost, cmc, type_line, printed_type_line, oracle_text, printed_text, power, toughness, set_id, `number`, rarity, gatherer_url, loyalty, produced_mana, other_face)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                    card["id_2"], card["oracle_id_2"], card["name"], card["printed_name_2"], card["lang"],
                    card["released_at"],
                    card["scryfall_uri"], card["mana_cost_2"], card["cmc_2"], card["type_line_2"],
                    card["printed_type_line_2"],
                    card["oracle_text_2"], card["printed_text_2"], card["power_2"], card["toughness_2"], card["set_id"],
                    card["collector_number"], card["rarity"], card["gatherer"], card["loyalty_2"],
                    card["produced_mana_2"],
                    card["other_face_2"]))
                cursor.execute(
                    "INSERT INTO image_uris (scryfall_id, small, normal, large, png, art_crop, border_crop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (card["id_2"], card["img_small_2"], card["img_normal_2"], card["img_large_2"], card["img_png_2"],
                     card["img_art_crop_2"], card["img_border_crop_2"]))


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


import_sets()
print("Sets importés ")
import_cards()
print("Cartes importées ")

# Valider les modifications et fermer la connexion
conn.commit()
conn.close()
