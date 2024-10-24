from flask import ( Blueprint, render_template )
from flaskr.db import get_db

bp = Blueprint("dataviz", __name__, url_prefix="/dataviz")

@bp.route("/", methods=["GET"])
def dataviz():

    db = get_db()

    rows = db.execute(
        """SELECT co.invoice_nb, strftime(co.invoice_date) as invoice_date, c.country, o.quantity, p.price, p.description 
        FROM order_detail as o 
        JOIN product as p 
        ON o.product_id == p.id 
        JOIN customer_order as co 
        ON o.order_id == co.id 
        JOIN customer as c 
        ON co.customer_id == c.id 
        LIMIT 50;"""
    ).fetchall()

    return render_template("/all.html", rows=rows)

@bp.route("/customer", methods=["GET"])
def customer():

    db = get_db()

    rows = db.execute(
        "SELECT id, country FROM customer LIMIT 50;"
    ).fetchall()

    return render_template("/customer.html", rows=rows)

@bp.route("/customer_order", methods=["GET"])
def customer_order():

    db = get_db()

    rows = db.execute(
        "SELECT id, invoice_nb, strftime(invoice_date) as invoice_date, customer_id FROM customer_order LIMIT 50;"
    ).fetchall()

    return render_template("/customer_order.html", rows=rows)

@bp.route("/product", methods=["GET"])
def product():

    db = get_db()

    rows = db.execute(
        "SELECT id, description, price FROM product LIMIT 50;"
    ).fetchall()

    return render_template("/product.html", rows=rows)

@bp.route("/order_detail", methods=["GET"])
def order_detail():

    db = get_db()

    rows = db.execute(
        "SELECT id, quantity, order_id, product_id FROM order_detail LIMIT 50;"
    ).fetchall()

    return render_template("/order_detail.html", rows=rows)

@bp.route("/pib", methods=["GET"])
def pib():
    db = get_db()

    rows = db.execute(
        "SELECT rank, country, pib FROM country_pib;"
    ).fetchall()

    return render_template("/pib.html", rows=rows)