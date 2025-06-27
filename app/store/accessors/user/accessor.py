from typing import Optional

from store.accessors.user.exceptions import UserDuplicateException
from store.accessors.user.models import UserModel
from store.database.postgres.accessor import BaseAccessor


class UserAccessor(BaseAccessor):
    class Meta:
        model = UserModel
        duplicate = UserDuplicateException

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        query = self.accessor.get_query_select_by_model(self.Meta.model).filter(self.Meta.model.email == email).limit(1)
        result = await self.accessor.query_execute(query)
        return result.one_or_none()
