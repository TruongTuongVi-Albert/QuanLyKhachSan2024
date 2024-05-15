import math

from flask import render_template, request, redirect, session, jsonify
import dao
import utils
from SystemDesign import app, admin, login
from flask_login import login_user, current_user, logout_user, login_required
import cloudinary.uploader
from decorators import loggedin


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    categories = dao.load_categories()
    products = dao.load_products(q, cate_id, page=page)
    return render_template('index.html', categories=categories, products=products,
                           page=math.ceil(dao.count_products() / app.config['PAGE_SIZE']))


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.route('/login', methods=['GET', 'POST'])
@loggedin
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

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Tên đăng nhập không hợp lệ!'

    return render_template('login.html', err_msg=err_msg)


@app.route("/logout", methods=['GET'])
def logout_my_user():
    logout_user()
    return redirect("/login")


@app.route('/intro')
def intro():
    return render_template('intro.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route('/api/carts', methods=['post'])  # Để thêm sp vào giỏ
def add_to_cart():
    """
    {
        "cart": {
            "1": {
                "id": "",
                "name": "...",
                "price": "...",
                "quantity": 1
                "quantityRoom": 1
                "checkInDate": "..."
                "checkOutDate": "..."
            }, "2": {
                "name": "...",
                "price": "...",
                "quantity": 1
                "quantityRoom": 1
                "checkOutDate": "..."
            }
        }
    }
    :return:
    """
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        # Trường hợp sp đã có trong giỏ rồi, lấy nó ra
        if cart[id]['quantity'] >= 1:
            cart[id]['quantity'] -= 1
        else:
            cart[id]['quantity'] += 1
    else:
        # Thêm phần tử vào từ điển (Thêm mới sp vào giỏ)
        cart[id] = {
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1,
            "check_in_date": request.json.get('check_in_date'),
            "check_out_date": request.json.get('check_out_date'),
        }
    # Cập nhật giỏ
    session['cart'] = cart

    # api lun trả về json
    # Thống kê kết quả trả về, hiện lên giao diện
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        cart[product_id]['quantityRoom'] = request.json['quantityRoom']
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@app.route("/register", methods=['get', 'post'])
@loggedin
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            dao.add_user(name=request.form.get('name'),
                         username=request.form.get('username'),
                         password=password,
                         avatar=avatar_path)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/rent', methods=['get', 'post'])
def rent():
    return render_template('rent.html')


@app.route("/book_room", methods=['get', 'post'])
def book_room():
    if request.method.__eq__('POST'):
        pass
    return render_template('book_room.html')


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except Exception as ex:
        print(ex)
        raise Exception({'status': 500})
    else:
        del session['cart']
        return jsonify({'status': 200})


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
