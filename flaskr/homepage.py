from flask import Blueprint, g, render_template
from flaskr import get_db, execute_db
import json
bp = Blueprint("homepage", __name__)

@bp.route("/")

def index():

    return render_template("homepage/index.html")



@app.route("/commands")
def command():
    db = get_db()
    product = 11111
    textfield = "Hello, this is a long textfield of different size to test if this kind of functionality works"
    execute_db(
    """
    INSERT INTO TABLE product(product, textfield) VALUES (%s, %s)
    """, (product, textfield)
    )
    db.commit()
    print("Worked")
    return json.dumps("An error has occured")