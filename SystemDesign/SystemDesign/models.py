from datetime import datetime
from enum import Enum as RoleEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Date, Boolean, DateTime
from sqlalchemy.orm import relationship

from SystemDesign import db, app


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2
    RECEPTIONIST = 3
    ACCOUNTANT = 4


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    rents = relationship('Rent', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship('Product', backref="category", lazy=True)

    def __repr__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://owa.bestprice.vn/images/hotels/large/terracotta-hotel-resort-da-lat-64ca10e5df84f-848x477.jpg')
    status = Column(String(20), default='Phòng trống')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)
    rents = relationship('Rent', backref='product', lazy=True)

    def __repr__(self):
        return self.name


class BookRoom(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity_customer = Column(Integer)
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    status = Column(String(3), default='no')

    def __repr__(self):
        return self.name


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Receipt(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(Base):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


class Rent(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    nationality = Column(String(50), nullable=False)
    CCCD = Column(String(50), unique=True, nullable=False)
    passport = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50), nullable=False)



if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        c1 = Category(name='Phòng đơn')
        c2 = Category(name='Phòng đôi đơn giản')
        c3 = Category(name='Phòng đôi cao cấp')
        c4 = Category(name='Phòng ba')
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        import json

        with open('data/products.json', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                prod = Product(**p)
                db.session.add(prod)

            db.session.commit()

        import hashlib

        u1 = User(name='admin', username='admin',
                  avatar='https://static.vecteezy.com/system/resources/previews/020/429/953/non_2x/admin-icon-vector.jpg',
                  password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                  user_role=UserRole.ADMIN)

        u2 = User(name='caodat', username='123456',
                  avatar='https://static.vecteezy.com/system/resources/previews/020/429/953/non_2x/admin-icon-vector.jpg',
                  password=str(hashlib.md5("12345678".encode('utf-8')).hexdigest()),
                  user_role=UserRole.USER)

        u3 = User(name='receptionist', username='receptionist',
                  avatar='https://i.pngimg.me/thumb/f/720/c3f2c592f9.jpg',
                  password=str(hashlib.md5("1234567".encode('utf-8')).hexdigest()),
                  user_role=UserRole.RECEPTIONIST)

        u4 = User(name='accountant', username='accountant',
                  avatar='https://cdn-icons-png.flaticon.com/512/1724/1724930.png',
                  password=str(hashlib.md5("123456789".encode('utf-8')).hexdigest()),
                  user_role=UserRole.ACCOUNTANT)
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()
