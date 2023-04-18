from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Product
from .secret import admin



views = Blueprint('views', __name__)


@views.route('/')
def home():
    products = Product.query.all()
    return render_template("home.html", products=products, user=current_user, admin=admin)

@views.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get(id)
    return render_template('product_details.html', product=product, user=current_user, admin=admin)





