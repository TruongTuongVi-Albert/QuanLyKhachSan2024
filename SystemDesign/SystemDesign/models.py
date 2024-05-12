from enum import Enum as RoleEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

from SystemDesign import db, app


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

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
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # c1 = Category(name='Phòng đơn')
        # c2 = Category(name='Phòng đôi đơn giản')
        # c3 = Category(name='Phòng đôi cao cấp')
        # c4 = Category(name='Phòng ba')
        # db.session.add_all([c1, c2, c3, c4])
        # db.session.commit()
        #
        # import json
        # with open('data/products.json', encoding='utf-8') as f:
        #     products = json.load(f)
        #     for p in products:
        #         prod = Product(**p)
        #         db.session.add(prod)
        #
        #     db.session.commit()

        import hashlib
        # u = User(name='admin', username='admin',
        #          avatar='https://static.vecteezy.com/system/resources/previews/020/429/953/non_2x/admin-icon-vector.jpg',
        #          password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        u2 = User(name='caodat', username='123456',
                  avatar='https://static.vecteezy.com/system/resources/previews/020/429/953/non_2x/admin-icon-vector.jpg',
                  password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                  user_role=UserRole.USER)
        db.session.add(u2)
        db.session.commit()
