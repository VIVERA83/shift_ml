from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.requests import Request

from admin.views import UserAdmin, SalaryAdmin
from core.lifespan import store
from core.settings import PostgresSettings
from store.store import Store


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str, _store: Store):
        super().__init__(secret_key)
        self._store = _store

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["email"], form["password"]

        if user := await self._store.accessor.user.get_by_email(email):
            if user.role == "admin" and self._store.accessor.token.verify_password(
                password, user.password
            ):
                access_token = self._store.accessor.token.create_access_token(user.id)
                request.session.update({"token": access_token})
                return True
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        if token := request.session.get("token"):
            return bool(self._store.accessor.token.verify_token(token))
        return False


def setup_admin(app, secret_key: str) -> None:
    engine = create_async_engine(
        PostgresSettings().dsn(True),
        echo=True,
        future=True,
    )
    authentication_backend = AdminAuth(secret_key=secret_key, _store=store)
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(SalaryAdmin)
