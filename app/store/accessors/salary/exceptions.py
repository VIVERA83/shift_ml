from store.database.postgres.exceptions import ExceptionBase


class UserDuplicateException(ExceptionBase):
    args = (
        "На данную дату уже назначено изменение зарплаты. Удалите запись или измените дату.",
    )
    code = 400

class NotFoundException(ExceptionBase):
    args = ("Пользователь с указанным идентификатором не найден.",)
    code = 404
