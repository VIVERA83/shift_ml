from store.database.postgres.exceptions import ExceptionBase


class UserDuplicateException(ExceptionBase):
    args = "На данную дату уже назначено изменение зарплаты. Удалите запись или измените дату."

    code = 400


class NotFoundException(ExceptionBase):
    args = "На данного сотрудника, записей по зарплате нет"
    code = 404
