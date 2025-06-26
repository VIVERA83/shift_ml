from datetime import date

from icecream import ic
from sqlalchemy import and_

from .exceptions import UserDuplicateException, NotFoundException
from .models import SalaryModel
from store.database.postgres.accessor import BaseAccessor


class SalaryAccessor(BaseAccessor):
    class Meta:
        model = SalaryModel
        duplicate = UserDuplicateException
        not_found = NotFoundException

    async def get_current_salary(self, user_id: int):
        query = (
            self.accessor.get_query_select_by_fields("*")
            .filter(
                and_(self.model.user_id == user_id, self.model.date <= date.today())
            )
            .order_by(self.Meta.model.date.desc())
            .limit(1)
        )
        result = await self.accessor.query_execute(query)
        if salary := result.mappings().one_or_none():
            return self.Meta.model(**salary)
        return None
