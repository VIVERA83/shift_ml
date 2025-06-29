from datetime import date

from sqlalchemy import and_

from store.database.postgres.accessor import BaseAccessor
from .exceptions import UserDuplicateException, NotFoundException
from .models import SalaryModel


class SalaryAccessor(BaseAccessor):
    class Meta:
        model = SalaryModel
        duplicate = UserDuplicateException
        not_found = NotFoundException

    @BaseAccessor._exception_handler
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

        salary = result.mappings().one()
        return self.Meta.model(**salary)

    @BaseAccessor._exception_handler
    async def get_next_date_change(self, user_id: int):
        query = (
            self.accessor.get_query_select_by_fields(self.Meta.model.date)
            .filter(and_(self.model.user_id == user_id, self.model.date > date.today()))
            .order_by(self.Meta.model.date.asc())
            .limit(1)
        )
        result = await self.accessor.query_execute(query)
        if salary := result.mappings().one_or_none():
            return salary
        return None
