import math

from flask import render_template, request, redirect
import dao
from SystemDesign import app, admin, login
from flask_login import login_user, current_user, logout_user


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    categories = dao.load_categories()
    products = dao.load_products(q, cate_id, page=page)
    return render_template('index.html', categories=categories, products=products,
                           page=math.ceil(dao.count_products()/app.config['PAGE_SIZE']))


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if dao.auth_user(username=username, password=password):
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Tên đăng nhập không hợp lệ!'

    return render_template('login.html', err_msg=err_msg)


@app.route("/logout", methods=['GET'])
def logout_my_user():
    logout_user()
    return redirect("/login")


@app.route('/intro')
def intro():
    product = dao.get_product_by_id(product_id=id)
    return render_template('intro.html', product=product)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/admin-login", methods=['POST'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')



if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
