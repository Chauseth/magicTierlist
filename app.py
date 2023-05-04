from flask import Flask, render_template, abort, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)


def get_db_connection():
    conn = mysql.connector.connect(user=os.getenv("DB_USER"),
                                   password=os.getenv("DB_PASSWORD"),
                                   host=os.getenv("DB_HOST"),
                                   database=os.getenv("DB_NAME"),
                                   raise_on_warnings=True)
    return conn


def fetchall_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetchone_dict(cursor):
    row = cursor.fetchone()
    if row is None:
        return None

    column_names = [desc[0] for desc in cursor.description]
    return {column_name: row[i] for i, column_name in enumerate(column_names)}


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    select distinct s.id , s.name, code, icon_svg_uri , s.released_at 
    from `sets` s 
    inner join cards c on s.id = c.set_id 
    where set_type in ('expansion', 'masterpiece', 'commander') order by s.released_at desc
    """)
    extensions = fetchall_dict(cursor)

    cursor.execute("""
    SELECT t.id, t.name, s.name as set_name,s.code, s.icon_svg_uri, t.created_at 
    FROM tierlists t  
    INNER JOIN `sets` s  ON t.set_id = s.id 
    ORDER BY t.created_at DESC 
    LIMIT 10
    """)
    tierlists = fetchall_dict(cursor)

    conn.close()
    return render_template('index.html', extensions=extensions, tierlists=tierlists)


@app.route('/extension/<string:extension_code>')
def extension(extension_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sets WHERE code = %s', (extension_code,))
    extension = fetchone_dict(cursor)

    cursor.execute('SELECT * FROM tierlists WHERE set_id = %s', (extension['id'],))
    tierlists = fetchall_dict(cursor)

    conn.close()
    return render_template('extension.html', extension=extension, tierlists=tierlists)


@app.route('/extension/<string:extension_code>/create_tierlist', methods=('GET', 'POST'))
def create_tierlist(extension_code):
    if request.method == 'POST':
        tierlist_name = request.form['name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM sets WHERE code = %s', (extension_code,))
        set_id_dict = fetchone_dict(cursor)
        set_id = set_id_dict["id"]

        cursor.execute('INSERT INTO tierlists (name, set_id) VALUES (%s, %s)', (tierlist_name, set_id))
        conn.commit()
        conn.close()
        return redirect(url_for('extension', extension_code=extension_code))

    return render_template('create_tierlist.html')


@app.route('/extension/<string:extension_code>/tierlist/<int:tierlist_id>')
def tierlist(extension_code, tierlist_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sets WHERE code = %s', (extension_code,))
    extension = fetchone_dict(cursor)

    cursor.execute('SELECT * FROM tierlists WHERE id = %s', (tierlist_id,))
    tierlist = fetchone_dict(cursor)

    cursor.execute(
        """
        SELECT DISTINCT cards.*, image_uris.normal, cards_ratings.rating
        FROM cards
        INNER JOIN image_uris ON cards.scryfall_id = image_uris.scryfall_id
        LEFT JOIN cards_ratings ON cards.id = cards_ratings.card_id AND cards_ratings.tierlist_id = %s
        WHERE cards.set_id = %s
        ORDER BY `number`
        """,
        (tierlist["id"], extension["id"])
    )
    cards = fetchall_dict(cursor)

    conn.close()
    return render_template('tierlist.html', extension=extension, tierlist=tierlist, cards=cards)


@app.route('/extension/<string:extension_code>/<int:tierlist_id>/save', methods=['POST'])
def save_tierlist_ratings(extension_code, tierlist_id):
    # Récupérer les données du formulaire
    ratings = {k.split("_")[1]: v for k, v in request.form.items() if k.startswith("rating_")}

    # Insérer les notes dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    for card_id, rating in ratings.items():
        cursor.execute(
            """
            INSERT INTO cards_ratings (card_id, tierlist_id, rating) VALUES (%s, %s, %s) AS new_row
            ON DUPLICATE KEY UPDATE rating = %s""",
            (card_id, tierlist_id, rating, rating)
        )

    conn.commit()
    conn.close()

    # Rediriger vers la page de la tierlist
    return redirect(url_for('tierlist', extension_code=extension_code, tierlist_id=tierlist_id))


@app.route('/card/<string:scryfall_id>')
def card(scryfall_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT cards.*, image_uris.png, sets.name as set_name, sets.code as set_code, sets.icon_svg_uri as set_icon
        FROM cards
        INNER JOIN image_uris ON cards.scryfall_id = image_uris.scryfall_id
        INNER JOIN sets ON cards.set_id = sets.id
        WHERE cards.scryfall_id = %s
        LIMIT 1
        """,
        (scryfall_id,))
    card = fetchone_dict(cursor)

    conn.close()
    return render_template('card.html', card=card)


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
