from flask import Flask, render_template, abort, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('cartes_magic.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    extensions = conn.execute(
        "SELECT DISTINCT sets.id, sets.name, code, icon_svg_uri FROM sets INNER JOIN cards ON sets.id = cards.set_id WHERE set_type in ('expansion', 'masterpiece', 'commander') ORDER BY sets.released_at DESC").fetchall()

    tierlists = conn.execute(
        "SELECT tierlists.id, tierlists.name, sets.name as set_name,sets.code, sets.icon_svg_uri FROM tierlists INNER JOIN sets ON tierlists.set_id = sets.id ORDER BY created_at DESC LIMIT 10").fetchall()
    conn.close()
    return render_template('index.html', extensions=extensions, tierlists=tierlists)


@app.route('/extension/<string:extension_code>')
def extension(extension_code):
    conn = get_db_connection()
    extension = conn.execute('SELECT * FROM sets WHERE code = ?', (extension_code,)).fetchone()
    tierlists = conn.execute('SELECT * FROM tierlists WHERE set_id = ?', (extension['id'],)).fetchall()
    conn.close()
    return render_template('extension.html', extension=extension, tierlists=tierlists)


@app.route('/extension/<string:extension_code>/create_tierlist', methods=('GET', 'POST'))
def create_tierlist(extension_code):
    if request.method == 'POST':
        tierlist_name = request.form['name']
        conn = get_db_connection()
        set_id = conn.execute('SELECT id FROM sets WHERE code = ?', (extension_code,)).fetchone()[0]
        conn.execute('INSERT INTO tierlists (name, set_id) VALUES (?, ?)', (tierlist_name, set_id))
        conn.commit()
        conn.close()
        return redirect(url_for('extension', extension_code=extension_code))

    return render_template('create_tierlist.html')


@app.route('/extension/<string:extension_code>/tierlist/<int:tierlist_id>')
def tierlist(extension_code, tierlist_id):
    conn = get_db_connection()
    extension = conn.execute('SELECT * FROM sets WHERE code = ?', (extension_code,)).fetchone()
    tierlist = conn.execute('SELECT * FROM tierlists WHERE id = ?', (tierlist_id,)).fetchone()
    cards = conn.execute(
        """
        SELECT cards.*, image_uris.normal, card_ratings.rating
        FROM cards
        INNER JOIN image_uris ON cards.scryfall_id = image_uris.scryfall_id
        LEFT JOIN card_ratings ON cards.id = card_ratings.card_id AND card_ratings.tierlist_id = ?
        WHERE cards.set_id = ?
        ORDER BY number
        """,
        (tierlist["id"], extension["id"])
    ).fetchall()

    conn.close()
    return render_template('tierlist.html', extension=extension, tierlist=tierlist, cards=cards)


@app.route('/extension/<string:extension_code>/<int:tierlist_id>/save', methods=['POST'])
def save_tierlist_ratings(extension_code, tierlist_id):
    # Récupérer les données du formulaire
    ratings = {k.split("_")[1]: v for k, v in request.form.items() if k.startswith("rating_")}

    # Insérer les notes dans la base de données
    conn = get_db_connection()
    for card_id, rating in ratings.items():
        conn.execute(
            """
            INSERT INTO card_ratings (card_id, tierlist_id, rating) VALUES (?, ?, ?)
            ON CONFLICT (card_id, tierlist_id) DO UPDATE SET rating = ?""",
            (card_id, tierlist_id, rating, rating)
        )
    conn.commit()
    conn.close()

    # Rediriger vers la page de la tierlist
    return redirect(url_for('tierlist', extension_code=extension_code, tierlist_id=tierlist_id))


@app.route('/card/<string:scryfall_id>')
def card(scryfall_id):
    conn = get_db_connection()
    card = conn.execute(
        """
        SELECT cards.*, image_uris.normal, sets.name as set_name, sets.code as set_code, sets.icon_svg_uri as set_icon
        FROM cards
        INNER JOIN image_uris ON cards.scryfall_id = image_uris.scryfall_id
        INNER JOIN sets ON cards.set_id = sets.id
        WHERE cards.scryfall_id = ?
        LIMIT 1
        """,
        (scryfall_id,)).fetchone()
    conn.close()
    return render_template('card.html', card=card)


if __name__ == '__main__':
    app.run(debug=True)
