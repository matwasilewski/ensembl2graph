from .config import settings

import datetime
import logging
import logging.handlers
import os
from typing import Optional

import ujson
from json_log_formatter import JSONFormatter

from .exceptions import BadLogFormatError

GREY = "\x1b[38;21m"
RED = "\x1b[31;21m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"

DEBUG = GREY + "{}" + RESET
INFO = GREY + "{}" + RESET
WARNING = RED + "{}" + RESET
ERROR = RED + "{}" + RESET
CRITICAL = BOLD_RED + "{}" + RESET


class ColourfulFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    FORMATS = {
        logging.DEBUG: DEBUG,
        logging.INFO: INFO,
        logging.WARNING: WARNING,
        logging.ERROR: ERROR,
        logging.CRITICAL: CRITICAL,
    }

    def format(self, record: logging.LogRecord) -> str:
        _log_fmt = self.FORMATS.get(record.levelno)
        if not _log_fmt:
            raise BadLogFormatError
        log_fmt = _log_fmt.format(self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomisedJSONFormatter(JSONFormatter):
    # Serialise datetime as timestamp by using ujson (which does it by default)
    # and disable ISO8601 date mutation:
    json_lib = ujson

    def json_record(
        self,
        message: str,
        extra: dict,
        record: logging.LogRecord,
    ) -> dict:
        extra['message'] = message

        # Include builtins
        extra['level'] = record.levelname
        extra['name'] = record.name
        extra['pathname'] = record.pathname
        extra['lineno'] = record.lineno

        if 'time' not in extra:
            extra['time'] = datetime.datetime.now()

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
        return extra


class CustomisedVerboseJSONFormatter(CustomisedJSONFormatter):
    def json_record(
        self,
        message: str,
        extra: dict,
        record: logging.LogRecord,
    ) -> dict:
        extra['funcName'] = record.funcName
        extra['module'] = record.module
        extra['pathname'] = record.pathname
        extra['process'] = record.process
        extra['processName'] = record.processName
        if hasattr(record, 'stack_info'):
            extra['stack_info'] = record.stack_info
        else:
            extra['stack_info'] = None
        extra['thread'] = record.thread
        extra['threadName'] = record.threadName
        return super(CustomisedVerboseJSONFormatter, self).json_record(
            message,
            extra,
            record,
        )


def get_logger(
    name: str,
    log_level: str,
    log_file: Optional[str] = None,
    sys_log: Optional[str] = None,
    verbose: bool = False,
    as_json: bool = False,
) -> logging.Logger:
    log_level = log_level.upper()
    logger = logging.getLogger(name)
    level = logging.getLevelName(log_level)

    if as_json:
        if verbose:
            formatter = CustomisedVerboseJSONFormatter()
        else:
            formatter = CustomisedJSONFormatter()
    else:
        fmt = "%(asctime)s - %(levelname)s - %(message)s "
        fmt += "(%(name)s; %(filename)s:%(lineno)d)"
        formatter = ColourfulFormatter(fmt)  # type: ignore

    if log_file:
        parent_dir = os.path.dirname(log_file)
        os.makedirs(os.path.abspath(parent_dir), exist_ok=True)
        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if sys_log:
        syslog_handler = logging.handlers.SysLogHandler(address=sys_log)
        syslog_handler.setLevel(level)
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger


log = get_logger(
    name=os.path.basename(__file__),
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_DIR,
    sys_log=settings.SYSLOG_ADDR,
    verbose=settings.VERBOSE_LOGS,
    as_json=settings.JSON_LOGS,
)
