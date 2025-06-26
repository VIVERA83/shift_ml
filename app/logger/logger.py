import inspect
import logging
import sys

from .formatter import ColoredFormatter

class CustomLogger(logging.Logger):

    def __init__(self, level: int = 10):
        super().__init__(self.__class__.__name__, level=level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        self.addHandler(console_handler)

    def debug(self, msg: object, *args, **kwargs):
        if self.isEnabledFor(10):
            self.log(10, msg, *args, extra=self.__extra(), **kwargs)

    def info(self, msg: object, *args, **kwargs):
        if self.isEnabledFor(20):
            self.log(20, msg, *args, extra=self.__extra(), **kwargs)

    def warning(self, msg: object, *args, **kwargs):
        if self.isEnabledFor(30):
            self.log(30, msg, *args, extra=self.__extra(), **kwargs)

    def error(self, msg: object, *args, **kwargs):
        if self.isEnabledFor(40):
            self.log(40, msg, *args, extra=self.__extra(), **kwargs)

    @staticmethod
    def __extra():
        return {
            "custom_func": inspect.stack()[2].function,
            "custom_lineno": inspect.stack()[2].lineno,
            "custom_name": list(inspect.stack()[2].frame.f_locals.values())[0].__class__.__name__
        }
