from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
from flask_admin import Admin
import cloudinary

app = Flask(__name__)
app.secret_key = "@#%$(*&^$%$#@$%&^*%^&*^$%&^*^&*daddfasfcFEDASC"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:02072002@localhost/it02saledbv2?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)

admin = Admin(app=app, name="Quản Trị Viên", template_mode="bootstrap4")
cloudinary.config(cloud_name='dltxyzwzv', api_key='631158489536735', api_secret='xlZgeh65aa-p-vwRMFe6vQjWAng')
login = LoginManager(app=app)
