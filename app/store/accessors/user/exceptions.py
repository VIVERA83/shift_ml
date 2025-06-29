from store.database.postgres.exceptions import ExceptionBase


class UserDuplicateException(ExceptionBase):
    args = (
        "Пользователь с указанным email уже зарегистрирован. Введите другой email или авторизуйтесь.",
    )
    code = 400
