from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from SystemDesign.models import Category, Product, UserRole
from SystemDesign import app, db
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyProductView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_sortable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name', 'price']
    can_export = True


class MyCategoryView(AuthenticatedView):
    column_list = ['id', 'name', 'products']


class LogoutView(BaseView):  # Tạo view đăng xuất
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name='Open Hotel DaLat', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))