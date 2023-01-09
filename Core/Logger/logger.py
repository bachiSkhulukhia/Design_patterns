from abc import ABC


class Logger(ABC):
    def __init__(self, next_logger):
        self.__next_logger = next_logger

    def next_logger(self, message):
        pass

    def log(self, message):
        self.next_logger(message)

        if self.__next_logger is not None:
            self.__next_logger.log(message)
        else:
            return
