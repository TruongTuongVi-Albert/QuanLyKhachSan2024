from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from SystemDesign.models import Category, Product, UserRole, User
from SystemDesign import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime


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


class MyUserView(AuthenticatedView):
    column_list = ['id', 'name', 'user_role']
    column_filters = ['id', 'name', 'user_role']


class RentsView(BaseView):
    @expose('/')
    def rents(self):
        return self.render('admin/rent.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.RECEPTIONIST


class StatsView(BaseView):
    @expose('/')
    def index(self):
        revenue_by_prods = dao.stats_revenue_by_product(kw=request.args.get('kw'))
        revenue_by_period = dao.stats_revenue_by_period(year=request.args.get('year', datetime.now().year),
                                                            period=request.args.get('period', 'month'))

        return self.render('admin/stats.html',
                            revenue_by_prods=revenue_by_prods,
                            revenue_by_period=revenue_by_period)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ACCOUNTANT


class LogoutView(BaseView):  # Tạo view đăng xuất
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsMDView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.count_products_by_cate()
        return self.render('admin/statsMD.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ACCOUNTANT


admin = Admin(app, name='Open Hotel DaLat', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyUserView(User, db.session))
admin.add_view(RentsView(name='Lập phiếu thuê phòng'))
admin.add_view(StatsView(name='Thống kê báo cáo doanh thu'))
admin.add_view(StatsMDView(name='Thống kê báo cáo mật độ phòng'))
admin.add_view(LogoutView(name='Đăng xuất'))