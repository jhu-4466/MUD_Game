# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: logger helper
# Author: m14
# Created: 2023.04.12
# Description: logger helper
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/12    basic build
#    m14         v0.5         2023/04/16    more complete build
# -----------------------------


import logging


class LoggerHelper:
    """
    
    logger helper.
    
    Args:
        ____name____: logger name
        ____logger____: one logger five logs.
        ____filepath____: log file path.
        ____formatter____: log record ____formatter____.
    """
    def __init__(self, name):
        self.____name____ = name
        
        filepath = '../logs/'
        self.____filepath____ = filepath
        
        self.____formatter____ = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - line:%(lineno)d - %(message)s')
        
        self.initialize()
    
    def initialize(self):
        self.____logger____ = logging.Logger(self.____name____)
        self.____logger____.setLevel(logging.DEBUG)
        
        debug_file_handler = logging.FileHandler(self.____filepath____ + f'/{self.____name____}_DEBUG.log')
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(self.____formatter____)
        
        info_file_handler = logging.FileHandler(self.____filepath____ + f'/{self.____name____}_INFO.log')
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(self.____formatter____)
        
        warning_file_handler = logging.FileHandler(self.____filepath____ + f'/{self.____name____}_WARNING.log')
        warning_file_handler.setLevel(logging.WARNING)
        warning_file_handler.setFormatter(self.____formatter____)
        
        error_file_handler = logging.FileHandler(self.____filepath____ + f'/{self.____name____}_ERROR.log')
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(self.____formatter____)
        
        critical_file_handler = logging.FileHandler(self.____filepath____ + f'/{self.____name____}_CRITICAL.log')
        critical_file_handler.setLevel(logging.CRITICAL)
        critical_file_handler.setFormatter(self.____formatter____)
        
        self.____logger____.addHandler(debug_file_handler)
        self.____logger____.addHandler(info_file_handler)
        self.____logger____.addHandler(error_file_handler)
        self.____logger____.addHandler(warning_file_handler)
        self.____logger____.addHandler(critical_file_handler)
    
    @property
    def logger(self):
        return self.____logger____
    
    @property
    def formatter(self):
        return self.____formatter____
    
    @formatter.setter
    def formatter(self, format: logging.Formatter):
        self.____formatter____ = format
    
    def info(self, message):
        self.____logger____.info(message)
    
    def error(self, message):
        self.____logger____.error(message)
    
    def debug(self, message):
        self.____logger____.debug(message)
    
    def critical(self, message):
        self.____logger____.critical(message)
    
    def warning(self, message):
        self.____logger____.warning(message)