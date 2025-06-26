from store.accessors.user.exceptions import UserDuplicateException
from store.accessors.user.models import UserModel
from store.database.postgres.accessor import BaseAccessor


class UserAccessor(BaseAccessor):
    class Meta:
        model = UserModel
        duplicate = UserDuplicateException
