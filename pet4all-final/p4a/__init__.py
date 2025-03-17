from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from flask_wtf import CSRFProtect

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petforall3.db'

# Secret key
app.config['SECRET_KEY'] = '4364bfe534'

# image uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
images = UploadSet('images', IMAGES, default_dest=lambda app: app.config['UPLOAD_FOLDER'])
configure_uploads(app, (images,))

# CSRF protection
csrf = CSRFProtect(app)

# extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Login configuration
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from p4a import routes
