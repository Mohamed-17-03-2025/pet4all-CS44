import os.path
from flask import render_template, redirect, url_for, flash, request, send_from_directory, abort
from p4a import app, db
from p4a.models import Pet, User, Accessory
from p4a.forms import RegisterForm, LoginForm, PetListForm, PetForYouForm, AccessoryForm, RateUserForm, EditForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from ml_model import get_recommendations


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_page():
    form = PetListForm()

    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        breed = form.breed.data
        status = form.status.data
        price = form.price.data
        description = form.description.data
        image = form.image.data
        seller_phone = form.seller_phone.data

        # Create the Pet object
        pet = Pet(name=name, age=age, breed=breed, status=status, price=price,
                  description=description, seller=current_user, seller_phone=seller_phone)
        db.session.add(pet)
        db.session.commit()  # Commit to get the pet's ID

        # Process the image file
        if image:
            filename = f"{pet.id}.jpg"  # Or any other extension
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            pet.image_path = filename
            db.session.commit()

        flash('Pet added successfully!', 'success')
        return redirect(url_for('add_page'))

    return render_template('add.html', form=form)


@app.route('/buy')
def buy_page():
    # Filter pets with a non-null price
    pets = Pet.query.filter_by(status='Sell').all()
    return render_template('buy.html', pets=pets)


@app.route('/adopt')
def adopt_page():
    # Filter pets with status 'Adoption'
    pets = Pet.query.filter_by(status='Adoption').all()
    return render_template('adopt.html', pets=pets)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(name=form.name.data,
                           age=form.age.data,
                           username=form.username.data,
                           email=form.email.data,
                           password=form.password1.data
                           )
        db.session.add(create_user)
        db.session.commit()
        image = form.image.data

        if image:
            filename = f"u+{create_user.id}.jpg"  # Or any other extension
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            create_user.image_path = filename
            db.session.commit()

        login_user(create_user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There is an Error : {error}', 'danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.verify_password(form.password.data):
            login_user(attempted_user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home_page'))


@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend_page():
    form = PetForYouForm()

    recommendations_cluster = None
    recommendations_collab = None

    if request.method == 'POST' and form.validate_on_submit():
        # Gather form data and make predictions using your ML model
        user_data = {
            'grooming': form.grooming.data,
            'grooming_preference': form.grooming_preference.data,
            'minimal_grooming': form.minimal_grooming.data,
            'shedding': form.shedding.data,
            'shedding_preference': form.shedding_preference.data,
            'manage_shedding': form.manage_shedding.data,
            'energy_level': form.energy_level.data,
            'daily_exercise': form.daily_exercise.data,
            'outdoor_activities': form.outdoor_activities.data,
            'trainability': form.trainability.data,
            'obedience_training': form.obedience_training.data,
            'quick_learning': form.quick_learning.data,
            'demeanor': form.demeanor.data,
            'playful': form.playful.data,
            'reserved': form.reserved.data,
            'size_of_living_space': form.size_of_living_space.data,
            'preferred_size': form.preferred_size.data,
            'indoor_space': form.indoor_space.data,
        }

        # Make recommendations using the ML model
        recommendations_cluster, recommendations_collab = get_recommendations(user_data)

        print("Recommended Dog Breeds (Clustering):")
        print(recommendations_cluster)

        print("\nTop Similar Dog Breeds (Collaborative Filtering):")
        print(recommendations_collab)

        # Render the template with the recommendations
        return render_template('recommend.html', form=form,
                               recommendations_cluster=recommendations_cluster,
                               recommendations_collab=recommendations_collab)

    return render_template('recommend.html', form=form)


@app.route('/forum')
@login_required
def forum():
    return render_template('forum.html')


@app.route('/accessories')
def accessories_page():
    accessories = Accessory.query.all()
    return render_template('accessories_buy.html', accessories=accessories)


@app.route('/sell_accessory', methods=['GET', 'POST'])
@login_required
def sell_accessory_page():
    form = AccessoryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        image = form.image.data

        # Create an Accessory object
        accessory = Accessory(name=name, description=description, price=price, seller=current_user)
        db.session.add(accessory)
        db.session.commit()  # Commit to get the accessory's ID

        # Process the image file
        if image:
            filename = secure_filename(image.filename)
            filename = f"a+{accessory.id}.jpg"  # Or any other extension you prefer
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            accessory.image_path = filename
            db.session.commit()  # Update with image_path

        flash('Accessory added successfully!', 'success')
        return redirect(url_for('sell_accessory_page'))

    return render_template('accessories_sell.html', form=form)


@app.route('/seller/<int:owner_id>', methods=['GET', 'POST'])
def seller_profile(owner_id):
    seller = User.query.get_or_404(owner_id)
    pets_sold = Pet.query.filter_by(owner_id=owner_id).all()

    # Instantiate your RateUserForm class
    form = RateUserForm()

    if form.validate_on_submit():
        rating = int(form.rating.data)
        seller.rating = rating
        db.session.commit()
        return redirect(url_for('seller_profile', owner_id=owner_id))

    # Pass rating choices to the template
    rating_choices = [1, 2, 3, 4, 5]

    return render_template('user.html', seller=seller, pets_sold=pets_sold, form=form, rating_choices=rating_choices,
                           user=current_user)


@app.route('/pet/<int:pet_id>')
def pet_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet.html', pet=pet)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    user = User.query.options(db.joinedload(User.pets), db.joinedload(User.accessories_sold)).get_or_404(user_id)
    form = RateUserForm()

    if form.validate_on_submit():
        rating = int(form.rating.data)
        user.rating = rating
        db.session.commit()
        return redirect(url_for('user_profile', user_id=user_id))

    # Pass rating choices to the template
    rating_choices = [1, 2, 3, 4, 5]

    return render_template('user.html', user=user, form=form, rating_choices=rating_choices)


@app.route('/rate_user/<int:user_id>', methods=['POST'])
@login_required
def rate_user(user_id):
    user = User.query.get_or_404(user_id)

    if 'rating' not in request.form:
        flash('Please select a rating.', 'warning')
        return redirect(url_for('user_profile', user_id=user_id))

    new_rating = int(request.form['rating'])

    # Update the rating with average calculation
    if user.rating:
        current_rating = user.rating
        total_ratings = user.total_ratings or 1  # Avoid division by zero if this is the first rating
        user.rating = (current_rating * total_ratings + new_rating) / (total_ratings + 1)
        user.total_ratings = total_ratings + 1 # Increment the number of ratings

    else:
        user.rating = new_rating
        user.total_ratings = 1

    db.session.commit()
    flash('Rating updated!', 'success')  # Update the success message
    return redirect(url_for('user_profile', user_id=user_id))


@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)


@app.route('/add_comment/<int:user_id>', methods=['POST'])
@login_required
def add_comment(user_id):
    user = User.query.get_or_404(user_id)
    comment_text = request.form['comment']

    # Update the user's reviews
    if user.reviews:
        user.reviews += "\n" + comment_text
    else:
        user.reviews = comment_text

    db.session.commit()
    flash('Comment added!', 'success')
    return redirect(url_for('user_profile', user_id=user_id))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.age = form.age.data

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(image_path)

            # If the user had an old image, delete it (optional)
            if current_user.image_path:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.image_path)
                os.remove(old_image_path)

            current_user.image_path = filename  # Update image_path on User

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user_profile', user_id=current_user.id))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.age.data = current_user.age

    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.owner != current_user:
        abort(403)
    db.session.delete(pet)
    db.session.commit()
    flash('Pet deleted!', 'success')
    return redirect(url_for('user_profile', user_id=current_user.id))


@app.route('/delete_accessory/<int:accessory_id>', methods=['POST'])
@login_required
def delete_accessory(accessory_id):
    accessory = Accessory.query.get_or_404(accessory_id)
    if accessory.seller != current_user:
        abort(403)
    db.session.delete(accessory)
    db.session.commit()
    flash('Accessory deleted!', 'success')
    return redirect(url_for('user_profile', user_id=current_user.id))


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    for pet in current_user.pets:
        db.session.delete(pet)
    accessories_to_delete = Accessory.query.filter_by(seller_id=current_user.id).all()
    for accessory in accessories_to_delete:
        db.session.delete(accessory)
    db.session.delete(current_user)
    db.session.commit()

    flash('Your account has been deleted.', 'success')
    logout_user()
    return redirect(url_for('home_page'))
