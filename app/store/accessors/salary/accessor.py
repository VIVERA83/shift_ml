from .exceptions import UserDuplicateException, NotFoundException
from .models import SalaryModel
from store.database.postgres.accessor import BaseAccessor


class SalaryAccessor(BaseAccessor):
    class Meta:
        model = SalaryModel
        duplicate = UserDuplicateException
        not_found = NotFoundException
