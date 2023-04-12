# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: base logger
# Author: m14
# Created: 2023.04.12
# Description: base logger
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/12    basic build
# -----------------------------


import logging


formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - line:%(lineno)d - %(message)s')


class BaseLogger:
    def __init__(self, name):
        self._name = name
        
        filepath = './logs/'
        self._filepath = filepath
        
        self.initialize()
    
    def initialize(self):
        self._logger = logging.Logger(self._name)
        self._logger.setLevel(logging.DEBUG)
        
        debug_file_handler = logging.FileHandler(self._filepath + f'/{self._name}_DEBUG.log')
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(formatter)
        
        info_file_handler = logging.FileHandler(self._filepath + f'/{self._name}_INFO.log')
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(formatter)
        
        warning_file_handler = logging.FileHandler(self._filepath + f'/{self._name}_WARNING.log')
        warning_file_handler.setLevel(logging.WARNING)
        warning_file_handler.setFormatter(formatter)
        
        error_file_handler = logging.FileHandler(self._filepath + f'/{self._name}_ERROR.log')
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        
        critical_file_handler = logging.FileHandler(self._filepath + f'/{self._name}_CRITICAL.log')
        critical_file_handler.setLevel(logging.CRITICAL)
        critical_file_handler.setFormatter(formatter)
        
        self._logger.addHandler(debug_file_handler)
        self._logger.addHandler(info_file_handler)
        self._logger.addHandler(error_file_handler)
        self._logger.addHandler(warning_file_handler)
        self._logger.addHandler(critical_file_handler)
        
        return self._logger