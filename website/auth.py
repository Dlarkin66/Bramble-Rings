from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, session
from .models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import secret

auth = Blueprint('auth', __name__)

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


@auth.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = Product.query.get(product_id)
        total_price += item['price'] * item['quantity']
        cart_items.append({'product': product, 'quantity': item['quantity'], 'price': item['price']})
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, user=current_user)



@auth.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    cart = session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'name': product.name, 'price': product.price, 'quantity': 1}

    session['cart'] = cart

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
        image_url = request.form['image_url']
        image_url_2 = request.form['image_url_2']
        image_url_3 = request.form['image_url_3']
        image_url_4 = request.form['image_url_4']
        
        new_product = Product(name=name, price=price, description=description, image_url=image_url, image_url_2=image_url_2, image_url_3=image_url_3, image_url_4=image_url_4)
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
        image_url = request.form.get('image_url')
        image_url_2 = request.form.get('image_url_2')
        image_url_3 = request.form.get('image_url_3')
        image_url_4 = request.form.get('image_url_4')


        product.name = name
        product.description = description
        product.price = price
        product.image_url = image_url
        product.image_url_2 = image_url_2
        product.image_url_3 = image_url_3
        product.image_url_4 = image_url_4

        db.session.commit()

        flash('Product updated successfully!')
        return redirect(url_for('views.product_details', id=id))
    
    return render_template('edit_product.html', product=product, user=current_user)