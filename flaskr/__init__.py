from flask import Flask, g, current_app, render_template, request, redirect
import os
import psycopg2
import psycopg2.extras
import json

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

@app.route("/")

def index():

    return render_template("homepage/index.html")

@app.route("/commands")
def command():
    db = get_db()

    liste = query_db(
    """
    SELECT * FROM product;
    """
    )
    db.commit()
    print(liste)
    print("Worked")
    return json.dumps("An erro ccured")
@app.route("/command")
def executecommand():
    db = get_db()

    execute_db(
    """
    CREATE TABLE product (
    product TEXT UNIQUE NOT NULL,
    textfield TEXT,
    related TEXT,
    PRIMARY KEY (product)
    );
    """
    )
    db.commit()
    print("Worked")
    return json.dumps("An erro ccured")



@app.route("/products/<product>")
def get_product(product):
    print(product)
    statement = f"SELECT * from product WHERE product = '{product}';"
    response = query_db(statement)
    print(response)
    text = response[0][1].split("\r\n")
    related = response[0][2].split("\r\n")
    print(related)
    print(text)
    return render_template("product/index.html", response=response[0][0], text=text, related=related)


@app.route("/products/update")
def update_product_list():
    product = request.args.get("product")
    product = str(product)
    print(product)
    statement = f"SELECT product FROM product WHERE product LIKE '{product}%%'"
    response = query_db(statement)
    glorified_response = list()
    for i in response:
        glorified_response.append(i[0])
    print(glorified_response)

    return json.dumps(glorified_response)

@app.route("/create")
def create_product_page():
    return render_template("product/create.html")

@app.route("/createproduct", methods=("GET", "POST"))
def create_product():
    if request.method == "POST":
        product_id = request.form["product_id"]
        stepbystep = request.form["stepbystep"]
        related = request.form["related"]
        if related == "":
            db = get_db()
            execute_db(
                """
                INSERT INTO product VALUES (%s, %s)
                """, (product_id, stepbystep)
            )
            db.commit()

        if related != "":
            relatedlist = related.split("\r\n")
            relatedlist.append(product_id)
            for i in relatedlist:
                new_related_list = []
                for j in relatedlist:
                    if str(i) != str(j):
                        new_related_list.append(j)
                string_related_liste="\r\n".join(new_related_list)
                print(string_related_liste)
                print(f"regarding product: {i}, these are the related articles: {new_related_list}")
                db = get_db()
                execute_db(
                    """
                    INSERT INTO product (product, textfield, related)VALUES (%s, %s, %s)
                    """, (i, stepbystep, string_related_liste)
                )
                db.commit()
                
    return redirect("/")


if __name__ == "__main__":
    app.run()

