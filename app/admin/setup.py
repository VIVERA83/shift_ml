from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import create_async_engine

from admin.views import UserAdmin, SalaryAdmin
from core.settings import PostgresSettings



def setup_admin(app):
    engine = create_async_engine(
        PostgresSettings().dsn(True),
        echo=True,
        future=True,
    )
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(SalaryAdmin)
