from flask import Blueprint, render_template

bp = Blueprint("product", __name__)

@bp.route("/products/<product>")
def get_product(product):
    return render_template("product/index.html")


@bp.route("/products/update")
def update_product_list():
    pass
