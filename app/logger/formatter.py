import logging


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.DEBUG: "\033[36m",  # Cyan
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[41m",  # White on Red
    }

    RESET_CODE = "\033[0m"

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.base_format = (
            "%(asctime)s | "
            "%(levelcolor)s%(levelname)-8s%(reset)s| "
            "\033[34m%"
            "(custom_name)"
            "s:%(custom_func)"
            "s:%(custom_lineno)"
            "d%(reset)s | "
            "%(messagecolor)s%(message)s%(reset)s"
        )

    def format(self, record):
        # Устанавливаем цвета для уровня и сообщения
        record.levelcolor = self.COLOR_CODES.get(record.levelno, "")
        record.messagecolor = self.COLOR_CODES.get(record.levelno, "\033[37m")
        record.reset = self.RESET_CODE

        # Создаем временный форматтер с нужными цветами
        formatter = logging.Formatter(self.base_format, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
