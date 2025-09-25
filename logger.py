import logging
import os
from datetime import datetime, date
from logging.handlers import BaseRotatingHandler
from functools import lru_cache


class DailyFileHandler(BaseRotatingHandler):
    """每天生成一个新日志文件，文件名为日期.log"""
    def __init__(self, log_dir, encoding="utf-8"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.current_date = date.today()
        self.baseFilename = self._get_log_path(self.current_date)
        super().__init__(self.baseFilename, mode="a", encoding=encoding, delay=False)

    def _get_log_path(self, d: date):
        return os.path.join(self.log_dir, f"{d.strftime('%Y-%m-%d')}.log")

    def shouldRollover(self, record):
        today = date.today()
        return today != self.current_date

    def doRollover(self):
        self.stream.close()
        self.current_date = date.today()
        self.baseFilename = self._get_log_path(self.current_date)
        self.stream = self._open()


class SingletonLogger:
    def __init__(self, include_caller_info=True):
        self.logger = logging.getLogger("FishingBot")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not self.logger.handlers:
            log_dir = "logs"

            fmt = (
                '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s()] %(message)s'
                if include_caller_info
                else '[%(asctime)s] [%(levelname)s] %(message)s'
            )
            datefmt = "%Y-%m-%d %H:%M:%S"
            formatter = logging.Formatter(fmt, datefmt)

            # 每天一个新文件：logs/YYYY-MM-DD.log
            file_handler = DailyFileHandler(log_dir, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)


@lru_cache(maxsize=1)
def get_logger(include_caller_info=True):
    return SingletonLogger(include_caller_info).logger


logger = get_logger()
