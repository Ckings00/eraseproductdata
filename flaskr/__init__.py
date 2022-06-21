from flask import Flask, current_app, g
import os
import psycopg2
import psycopg2.extras


app = Flask(__name__)
DATABASE = os.environ['DATABASE_URL']
app.debug = True
app.secret_key = "debug"


def init_db(): #Fra Magnus forandret
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()

def get_db(): # Fra Magnus uforandret
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE)
    return db

def query_db(query, args=(), one=False): # Fra Magnus uforandret
    # 'INSERT INTO bar_table (name, capacity) VALUES (%s, %s)'
    # (str(name), int(capacity))
    cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=(), one=False): # Fra Magnus uforandret
    # 'INSERT INTO bar_table (name, capacity) VALUES (%s, %s)'
    # (str(name), int(capacity))
    cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, args)
    cur.close()



from . import homepage
app.register_blueprint(homepage.bp)
app.add_url_rule("/", endpoint="index")

from . import product
app.register_blueprint(product.bp)


if __name__ == "__main__":
    app.run()

