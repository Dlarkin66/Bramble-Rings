from flask import Blueprint, render_template
from flask_login import current_user
from .models import Product
from .secret import admin


views = Blueprint('views', __name__)


@views.route('/')
def home():
    products = Product.query.order_by(Product.order).all()

    return render_template(
        "home.html", 
        products=products, 
        user=current_user, 
        admin=admin
    )


@views.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get(id)

    return render_template(
        'product_details.html', 
        product=product, 
        user=current_user, 
        admin=admin
    )


@views.route('/about')
def about_me():
    return render_template(
        'about_me.html', 
        user=current_user
    )


@views.route('/faq')
def faq():
    return render_template(
        'faq.html', 
        user=current_user
    )







