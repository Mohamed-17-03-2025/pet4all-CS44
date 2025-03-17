import unittest
from io import BytesIO

from flask_testing import TestCase
from flask import Flask
from werkzeug.datastructures import FileStorage

from p4a import app, db
from p4a.forms import RegisterForm, LoginForm, PetListForm, PetForYouForm, AccessoryForm, RateUserForm, EditForm

class TestForms(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_form(self):
        # Create a test image file
        test_image_data = b"dummy data"
        test_image = BytesIO(test_image_data)
        test_image.name = "test_image.jpg"

        # Create a test form instance with valid data
        form = RegisterForm(name='Test User', age=25, username='testuser', email='test@example.com',
                            password1='password', password2='password', image=test_image)

        # Validate the form
        self.assertTrue(form.validate(), "Form validation failed. Errors: {}".format(form.errors))

    def test_login_form(self):
        form = LoginForm(username='testuser', password='password')
        self.assertTrue(form.validate())

    def test_pet_list_form(self):
        # Create a dummy image file for testing
        dummy_image = FileStorage(stream=BytesIO(b"dummy image data"), filename="dummy_image.jpg")

        # Create a test form instance with valid data and include the dummy image
        form = PetListForm(name='Test Pet', age=1, breed='German Shepherd', price=200,
                           seller_phone='1234567890', status='Sale', description='Test description',
                           image=dummy_image)

        # Validate the form
        self.assertTrue(form.validate(), form.errors)

    def test_pet_for_you_form(self):
        form = PetForYouForm()
        form.grooming.data = '0.5'
        form.grooming_preference.data = '0'
        form.minimal_grooming.data = '1'
        form.shedding.data = '0.5'
        form.shedding_preference.data = '0'
        form.manage_shedding.data = '1'
        form.energy_level.data = '0.5'
        form.daily_exercise.data = '1'
        form.outdoor_activities.data = '0'
        form.trainability.data = '1'
        form.obedience_training.data = '0'
        form.quick_learning.data = '0.5'
        form.demeanor.data = '1'
        form.playful.data = '0.5'
        form.reserved.data = '0'
        form.size_of_living_space.data = '1'
        form.preferred_size.data = '0.5'
        form.indoor_space.data = '0.5'
        self.assertTrue(form.validate())

    def test_accessory_form(self):
        # Create a test image file
        test_image = FileStorage(stream=BytesIO(b"dummy data"), filename="test_image.jpg")

        # Instantiate the form with the valid image
        form = AccessoryForm(name='Test Accessory', description='Test description', price=30, image=test_image)

        # Validate the form with the provided image
        self.assertTrue(form.validate(), form.errors)

    def test_rate_user_form(self):
        form = RateUserForm(rating=5, comment='Great seller!')
        self.assertTrue(form.validate())

    def test_edit_form(self):
        form = EditForm(name='New Name', username='newusername', email='newemail@example.com', age=30)
        self.assertTrue(form.validate())

    def test_rate_user_form_invalid_rating(self):
        # Test case: Invalid rating (rating greater than 5)
        form = RateUserForm(rating=6, comment='Great seller!')
        self.assertFalse(form.validate())

    def test_rate_user_form_empty_comment(self):
        # Test case: Invalid rating (empty comment)
        form = RateUserForm(rating=4, comment='')
        self.assertFalse(form.validate())

    def test_rate_user_form_missing_rating(self):
        # Test case: Invalid rating (rating not selected)
        form = RateUserForm(comment='Good seller!')
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
