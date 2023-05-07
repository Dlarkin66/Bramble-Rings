from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

from .models import User, Product
from . import db
from . import secret


auth = Blueprint('auth', __name__)
mail = Mail()


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else: 
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return  render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/add_to_cart/<int:product_id>', methods=["GET", "POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    cart = session.get('cart', {})
    ring_size = request.form.get("ring-size")

    if ring_size == None:
        flash('Please select a ring size.', category='error')
        return redirect(url_for('views.product_details', id=product_id))
    else:
        cart_key = str(product_id) + '_' + ring_size
        if cart_key in cart:
            cart[cart_key]['quantity'] += 1
        else:
            cart[cart_key] = {'name': product.name, 'price': product.price, 'quantity': 1, 'size': ring_size}
        flash('Item added to cart!', category='success')
    
    session['cart'] = cart
    return redirect(url_for('views.product_details', id=product_id))
 

@auth.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for cart_key, item in cart.items():
        product_id, ring_size = cart_key.split('_')
        product = Product.query.get(product_id)
        total_price += item['price'] * item['quantity']
        cart_items.append({'product': product, 'quantity': item['quantity'], 'price': item['price'], 'size': item['size']})
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, user=current_user, float=float)


@auth.route('/remove_from_cart/<int:product_id>/<float:product_size>', methods=["POST"])
@login_required
def remove_from_cart(product_id, product_size):
    cart = session.get('cart', {})
    if f"{product_id}_{product_size}" in cart:
        del cart[f"{product_id}_{product_size}"]
        session['cart'] = cart
        flash('Item removed from cart!', category='success')
        return redirect(url_for('auth.cart'))
    else:
        flash('There was an error removing the item, please refresh the page and try again.', category='error')
        return redirect(url_for('auth.cart'))

 

@auth.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.email != secret.admin:
        abort(403)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        materials = request.form.get('materials')
        image_url = request.form['image_url']
        image_url_2 = request.form['image_url_2']
        image_url_3 = request.form['image_url_3']
        image_url_4 = request.form['image_url_4']
        new_product = Product(name=name, price=price, description=description, materials=materials, image_url=image_url, image_url_2=image_url_2, image_url_3=image_url_3, image_url_4=image_url_4)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('views.home'))
    else:
        return render_template('add_product.html', user=current_user)
    

@auth.route('/remove_product/<int:id>', methods=['POST'])
@login_required
def remove_product(id):
    if current_user.email != secret.admin:
        abort(403)
    else:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('views.home'))


@auth.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get(id)

    if current_user.email != secret.admin:
        abort(403)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        materials = request.form.get('materials')
        image_url = request.form.get('image_url')
        image_url_2 = request.form.get('image_url_2')
        image_url_3 = request.form.get('image_url_3')
        image_url_4 = request.form.get('image_url_4')
        product.name = name
        product.description = description
        product.price = price
        product.materials = materials
        product.image_url = image_url
        product.image_url_2 = image_url_2
        product.image_url_3 = image_url_3
        product.image_url_4 = image_url_4
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('views.product_details', id=id))
    
    return render_template('edit_product.html', product=product, user=current_user)


@auth.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        msg = Message(
            subject=subject,
            sender=(name, email),
            reply_to=email, 
            recipients=['brambleringshelp@gmail.com'],
            body=message
        )

        if len(name) < 2:
            flash('Name must be longer than one character.', category='error')
        elif len(email) < 4:
            flash('Email must be longer than three characters.', category='error')
        elif len(message) < 20:
            flash('Message must be at least 20 characters in lenght.', category='success')
        else:
            flash('Message sent! I will get back to you shortly!', category='success')
            mail.send(msg)

    return render_template('contact.html', user=current_user)