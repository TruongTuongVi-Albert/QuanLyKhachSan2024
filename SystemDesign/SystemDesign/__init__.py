from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)


app.secret_key = '*&(@#!%^!$&*@1237643857#$%()&@81367'   # Làm session lun có secret_key. Vì session là đt sever nên cần mã hóa. Amdin
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/qlkhachsan?charset=utf8mb4" % quote('admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4

db = SQLAlchemy(app)
login = LoginManager(app)