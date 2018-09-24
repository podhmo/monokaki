import sys
import logging
from collections import ChainMap
from logging import (  # NOQA
    CRITICAL,
    FATAL,
    ERROR,
    WARNING,
    WARN,
    INFO,
    DEBUG,
    NOTSET,
)
from monokaki.renderer import DEFAULT_RENDERER


class StructLogger(logging.LoggerAdapter):
    def bind(self, **kwargs):
        return self.__class__(self.logger, ChainMap(kwargs, self.extra))

    def process(self, msg, kwargs):
        information = {
            "extra": {
                "kwargs": ChainMap(kwargs, self.extra),
                "structual": True,
            },
            "stack_info": kwargs.pop("stack_info", False),
            "exc_info": kwargs.pop("exc_info", False),
        }
        return msg, information


class StructuralFormatter:
    def __init__(self, formatter=None, renderer=None):
        self.formatter = formatter or logging.Formatter(logging.BASIC_FORMAT)
        self.renderer = renderer or DEFAULT_RENDERER

    def format(self, record):
        if not getattr(record, "structual", False):
            return self.formatter.format(record)
        d = {"msg": record.msg, "level": record.levelname}
        if record.exc_info:
            d["stack"] = self.formatter.formatException(record.exc_info)
        if record.stack_info:
            d["stack"] = self.formatter.formatStack(record.stack_info)
        d.update(record.kwargs)
        return self.renderer(d, record, self.formatter)


def get_logger(name):
    return StructLogger(logging.getLogger(name), {})


getLogger = get_logger  # backword compatibility of std logging


def basic_config(
    level,
    stream=None,
    formatter=None,
    format=logging.BASIC_FORMAT,
    renderer=DEFAULT_RENDERER,
    handlers=None,
):
    if handlers is None:
        stream = stream or sys.stderr
        handler = logging.StreamHandler(stream)
        formatter = formatter or StructuralFormatter(logging.Formatter(format), renderer=renderer)
        handler.setFormatter(formatter)
        handlers = [handler]
    logging.basicConfig(level=level, handlers=handlers)
