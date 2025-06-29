from sqladmin import ModelView

from store.accessors.salary.models import SalaryModel
from store.accessors.user.models import UserModel


class UserAdmin(ModelView, model=UserModel):
    name = "Сотрудник"
    name_plural = "Сотрудники"
    column_searchable_list = [
        UserModel.username,
        UserModel.email,
    ]
    column_sortable_list = [
        UserModel.username,
    ]
    column_list = [
        UserModel.id,
        UserModel.username,
        UserModel.email,
    ]
    column_labels = {
        UserModel.email: "Email",
        UserModel.username: "Фамилия Имя Отчество",
    }


class SalaryAdmin(ModelView, model=SalaryModel):
    name = "Зарплата"
    name_plural = "Зарплаты"
    column_labels = {
        SalaryModel.salary: "Зарплата",
        SalaryModel.date: "Дата назначения",
        SalaryModel.user_id: "ID сотрудника",
    }
    column_list = [
        SalaryModel.id,
        SalaryModel.salary,
        SalaryModel.date,
        SalaryModel.user_id,
    ]
    form_include_pk = True  # Важное изменение!

    # Или более гибкий вариант:
    form_columns = [
        SalaryModel.user_id,
        SalaryModel.salary,
        SalaryModel.date,
    ]  # Включаем id вручную
