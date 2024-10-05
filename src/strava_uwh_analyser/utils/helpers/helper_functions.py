import logging
from logging import getLogger
from typing import Optional, Literal


def add_logger(self, logger_level: Optional[Literal["debug", "info"]] = None):
    self.logger = getLogger(self.__name__)
    return self
    # if logger_level is not None:
    #     self.logger.setLevel(logger_level)
    # else:
    #     self.logger.setLevel(self.base_variables.logging_level)


def get_logging_level(
        logging_level: Literal["debug", "info"]
) -> logging:
    if logging_level == "debug":
        return logging.DEBUG
    elif logging_level == "info":
        return logging.INFO
    else:
        f"Logging level {logging_level} is not implemented"


