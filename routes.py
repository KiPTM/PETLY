from flask import render_template, redirect, url_for, flash, request
from app import app, db, login_manager
from models import User, Pet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from forms import PetForm, RegistrationForm, LoginForm

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
    form = RegistrationForm()
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
        print("User is already authenticated.")  # Debugging statement
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            print(f"User {user.username} logged in successfully.")  # Debugging statement
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            print("Invalid credentials entered.")  # Debugging statement
            flash('Invalid credentials!', 'danger')

    return render_template('login.html', form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

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
        # Save the message to the database or send an email
        flash('Message sent successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('contact.html')

@app.route('/pet/<int:pet_id>')
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)  # Return 404 if the pet doesn't exist
    return render_template('pet_detail.html', pet=pet)

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.owner != current_user:  # Ensure only the owner can edit the pet
        flash('You do not have permission to edit this pet listing.', 'danger')
        return redirect(url_for('home'))
    
    form = PetForm(obj=pet)  # Pre-fill the form with existing data
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.breed = form.breed.data
        pet.price = form.price.data
        pet.description = form.description.data
        db.session.commit()
        flash('Pet listing updated successfully!', 'success')
        return redirect(url_for('pet_detail', pet_id=pet.id))
    
    return render_template('edit_pet.html', form=form, pet=pet)

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.owner != current_user:  # Ensure only the owner can delete the pet
        flash('You do not have permission to delete this pet listing.', 'danger')
        return redirect(url_for('home'))
    
    db.session.delete(pet)
    db.session.commit()
    flash('Pet listing deleted successfully!', 'success')
    return redirect(url_for('browse_pets'))

@app.route('/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/about')
def about():
    return render_template('about.html', title='About PetNest')