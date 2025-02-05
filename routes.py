from flask import render_template, redirect, url_for, flash, request
from app import app, db, login_manager
from models import User, Pet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from forms import RegistrationForm, LoginForm, PetForm  # Import forms here

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html', title='Welcome to PetNest')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()  # Use the imported RegistrationForm
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()  # Use the imported LoginForm
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html', form=form)

# Add other routes here...

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/users')
@login_required
def view_users():
    if not current_user.is_admin:  # Add an `is_admin` field to your User model
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_pet():
    form = PetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            breed=form.breed.data,
            price=form.price.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('Pet listed successfully!', 'success')
        return redirect(url_for('browse_pets'))
    return render_template('sell.html', form=form)

@app.route('/browse')
def browse_pets():
    breed = request.args.get('breed', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    query = Pet.query
    if breed:
        query = query.filter(Pet.breed.ilike(f'%{breed}%'))
    if min_price is not None:
        query = query.filter(Pet.price >= min_price)
    if max_price is not None:
        query = query.filter(Pet.price <= max_price)
    pets = query.all()
    return render_template('browse.html', pets=pets)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Save to database or send email
        flash('Message sent successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html')