from sqladmin import Admin, ModelView

from core.lifespan import store
from store.accessors.user.models import UserModel


# Регистрируем модели
class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.username, UserModel.email]




def setup_admin(app):
    admin = Admin(app,store.database.postgres._engine)
    admin.add_view(UserAdmin)
