# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: singleton type
# Author: m14
# Created: 2023.04.11
# Description: a util for singleton type
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/11    basic build
# -----------------------------


import threading


class SingletonType(type):
    _instance_lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        # judge whether the instance exists.
        if not hasattr(cls, "_instance"):
            # to suit multithreading.
            with SingletonType._instance_lock:
                # make sure again before create the instance.
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance