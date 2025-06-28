from typing import Optional

from core.settings import AdminSettings
from store.accessors.user.exceptions import UserDuplicateException
from store.accessors.user.models import UserModel
from store.database.postgres.accessor import BaseAccessor


class UserAccessor(BaseAccessor):
    class Meta:
        model = UserModel
        duplicate = UserDuplicateException

    def __init__(self, settings: AdminSettings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings

    async def connect(self):
        try:
            await self.create(username=self.settings.username,
                              email=self.settings.admin_email,
                              password=self.settings.admin_password,
                              role="admin",
                              )
        except Exception as e:
            self.logger.error(e)

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        query = (
            self.accessor.get_query_select_by_model(self.Meta.model)
            .filter(self.Meta.model.email == email)
            .limit(1)
        )
        result = await self.accessor.query_execute(query)
        if users := result.first():
            return users[0]
        return None
