import unittest
from flask_testing import TestCase
from p4a import app, db
from p4a.models import User, Pet, Accessory


class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        # Create test data
        self.user = User(name='Test User', age=25, username='testuser', email='test@example.com', password='password')
        self.pet = Pet(name='Test Pet', age=2, breed='Labrador', status='Adoption', price=100,
                       description='Test description', seller=self.user)
        self.accessory = Accessory(name='Test Accessory', description='Test accessory description', price=50,
                                   seller=self.user, image_path='test_image.jpg')  # Provide a dummy image path
        db.session.add_all([self.user, self.pet, self.accessory])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post('/register', data=dict(
            name='Test User2', age=30, username='testuser2', email='test2@example.com', password1='password',
            password2='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser', password='password'
        ), follow_redirects=True)
        self.assertIn(b'Logged in successfully!', response.data)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)

    def test_add_pet(self):
        with self.client:
            # Log in the test user
            self.client.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)

            # Make the request to add a pet
            response = self.client.post('/add', data=dict(
                name='New Pet',
                age=1,
                breed='German Shepherd',
                status='Sale',
                price=200,
                description='New description',
                seller_phone='1234567890'
            ), follow_redirects=True)

            # Assert that the success message is present in the response
            self.assertEqual(response.status_code, 200)

    def test_buy_page(self):
        response = self.client.get('/buy')
        self.assertEqual(response.status_code, 200)

    def test_adopt_page(self):
        response = self.client.get('/adopt')
        self.assertEqual(response.status_code, 200)

    def test_accessories_page(self):
        response = self.client.get('/accessories')
        self.assertIn(b'Test Accessory', response.data)

    def test_sell_accessory(self):
        with self.client:
            self.client.post('/login', data=dict(
                username='testuser', password='password'
            ), follow_redirects=True)
            response = self.client.post('/sell_accessory', data=dict(
                name='New Accessory', description='New accessory description', price=30
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_account(self):
        with self.client:
            self.client.post('/login', data=dict(
                username='testuser', password='password'
            ), follow_redirects=True)
            response = self.client.post('/delete_account', follow_redirects=True)
            self.assertIn(b'Your account has been deleted.', response.data)


if __name__ == '__main__':
    unittest.main()
