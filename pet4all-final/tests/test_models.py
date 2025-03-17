import unittest
from p4a import db, app
from p4a.models import User, Pet, Accessory

class TestModels(unittest.TestCase):

    def setUp(self):
        # Create a test Flask application
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Check if user is added successfully
            self.assertEqual(User.query.count(), 1)

    def test_pet_creation(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test pet
            pet = Pet(name='Test Pet', age=1, breed='German Shepherd', status='Sale', price=200,
                      description='Test description', seller=user, seller_phone='1234567890')
            db.session.add(pet)
            db.session.commit()

            # Check if pet is added successfully
            self.assertEqual(Pet.query.count(), 1)

    def test_accessory_creation(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test accessory
            accessory = Accessory(name='Test Accessory', description='Test description', price=30, seller=user)
            db.session.add(accessory)
            db.session.commit()

            # Check if accessory is added successfully
            self.assertEqual(Accessory.query.count(), 1)

    def test_user_deletion(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            # Check if user is deleted successfully
            self.assertEqual(User.query.count(), 0)

    def test_pet_deletion(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test pet
            pet = Pet(name='Test Pet', age=1, breed='German Shepherd', status='Sale', price=200,
                      description='Test description', seller=user, seller_phone='1234567890')
            db.session.add(pet)
            db.session.commit()

            # Delete the pet
            db.session.delete(pet)
            db.session.commit()

            # Check if pet is deleted successfully
            self.assertEqual(Pet.query.count(), 0)

    def test_accessory_deletion(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test accessory
            accessory = Accessory(name='Test Accessory', description='Test description', price=30, seller=user)
            db.session.add(accessory)
            db.session.commit()

            # Delete the accessory
            db.session.delete(accessory)
            db.session.commit()

            # Check if accessory is deleted successfully
            self.assertEqual(Accessory.query.count(), 0)

    def test_user_password_verification(self):
        # Create a test user
        user = User(name='Test User', age=25, username='testuser', email='test@example.com')
        user.password = 'password'
        db.session.add(user)
        db.session.commit()

        # Verify correct password
        self.assertTrue(user.verify_password('password'))

        # Verify incorrect password
        self.assertFalse(user.verify_password('wrong_password'))

    def test_user_update(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Update the user's email
            user.email = 'updated_email@example.com'
            db.session.commit()

            # Retrieve the user from the database
            updated_user = User.query.filter_by(username='testuser').first()

            # Check if the user's email has been updated successfully
            self.assertEqual(updated_user.email, 'updated_email@example.com')

    def test_pet_update(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test pet
            pet = Pet(name='Test Pet', age=1, breed='German Shepherd', status='Sale', price=200,
                      description='Test description', seller=user, seller_phone='1234567890')
            db.session.add(pet)
            db.session.commit()

            # Update the pet's age
            pet.age = 2
            db.session.commit()

            # Retrieve the pet from the database
            updated_pet = Pet.query.filter_by(name='Test Pet').first()

            # Check if the pet's age has been updated successfully
            self.assertEqual(updated_pet.age, 2)

    def test_accessory_update(self):
        with app.app_context():
            # Create a test user
            user = User(name='Test User', age=25, username='testuser', email='test@example.com')
            user.password = 'password'
            db.session.add(user)
            db.session.commit()

            # Create a test accessory
            accessory = Accessory(name='Test Accessory', description='Test description', price=30, seller=user)
            db.session.add(accessory)
            db.session.commit()

            # Update the accessory's price
            accessory.price = 40
            db.session.commit()

            # Retrieve the accessory from the database
            updated_accessory = Accessory.query.filter_by(name='Test Accessory').first()

            # Check if the accessory's price has been updated successfully
            self.assertEqual(updated_accessory.price, 40)

if __name__ == '__main__':
    unittest.main()
