from flask import Flask, render_template, request
import dao


app = Flask(__name__)


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')

    categories = dao.load_categories()
    products = dao.load_products(q, cate_id)
    return render_template('index.html', categories=categories, products=products)


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
    return render_template('login.html')


@app.route('/intro')
def intro():
    return render_template('intro.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
