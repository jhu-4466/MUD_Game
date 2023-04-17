# -*- coding: utf-8 -*-

"""

NEW Changes
======================
Original 1: https://github.com/fyrestone/pydevd_reload
Original 2: https://github.com/fabioz/PyDev.Debugger/blob/main/_pydevd_bundle/pydevd_reload.py

add api for setting auto reload

======================
Based on the python xreload.

Changes
======================
1. we don't recreate the old namespace from new classes. Rather, we keep the existing namespace,
load a new version of it and update only some of the things we can inplace. That way, we don't break
things such as singletons or end up with a second representation of the same class in memory.
2. If we find it to be a __metaclass__, we try to update it as a regular class.
3. We don't remove old attributes (and leave them lying around even if they're no longer used).
4. Reload hooks were changed
These changes make it more stable, especially in the common case (where in a debug session only the
contents of a function are changed), besides providing flexibility for users that want to extend
on it.
Hooks
======================
Classes/modules can be specially crafted to work with the reload (so that it can, for instance,
update some constant which was changed).
1. To participate in the change of some attribute:
    In a module:
    __xreload_old_new__(namespace, name, old, new)
    in a class:
    @classmethod
    __xreload_old_new__(cls, name, old, new)
    A class or module may include a method called '__xreload_old_new__' which is called when we're
    unable to reload a given attribute.
2. To do something after the whole reload is finished:
    In a module:
    __xreload_after_reload_update__(namespace):
    In a class:
    @classmethod
    __xreload_after_reload_update__(cls):
    A class or module may include a method called '__xreload_after_reload_update__' which is called
    after the reload finishes.
Important: when providing a hook, always use the namespace or cls provided and not anything in the global
namespace, as the global namespace are only temporarily created during the reload and may not reflect the
actual application state (while the cls and namespace passed are).
Current limitations
======================
- Attributes/constants are added, but not changed (so singletons and the application state is not
  broken -- use provided hooks to workaround it).
- Code using metaclasses may not always work.
- Functions and methods using decorators (other than classmethod and staticmethod) are not handled
  correctly.
- Renamings are not handled correctly.
- Dependent modules are not reloaded.
- New __slots__ can't be added to existing classes.
Info
======================
Original: http://svn.python.org/projects/sandbox/trunk/xreload/xreload.py
Note: it seems https://github.com/plone/plone.reload/blob/master/plone/reload/xreload.py enhances it (to check later)
Interesting alternative: https://code.google.com/p/reimport/
Alternative to reload().
This works by executing the module in a scratch namespace, and then patching classes, methods and
functions in place.  This avoids the need to patch instances.  New objects are copied into the
target namespace.

Latest update in 2023.04.14 by chatgpt 3.5 and m14.
The neweset version is justed used for the MUD Game named SE produced by m14.
"""


import sys
import os
import time
import logging
import inspect


def setup():
    AutoReloader().setup()


def refresh():
    AutoReloader().refresh()


class AutoReloader:
    """_summary_
    
    The auto reloader api.

    Returns:
        _instance: one instance of the class.
    """    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._boot_time = 0
            cls._instance._module_mtime = {}
        return cls._instance

    def setup(self):
        """_summary_
        
        Set up the start reload time.
        
        """        
        self._boot_time = time.time()

    def refresh(self):
        """_summary_
        
        Refresh the module for one time.
        If you need to refresh for the whole time, you may implement the logic by yourself in the out layer.
        
        """ 
        reload_start_time = time.time()
        invalid_modules = self._get_invalid_module()
        for module in invalid_modules.values():
            xreload(module)
            # spec = importlib.util.spec_from_file_location(module_name, module_path)
            # module = importlib.util.module_from_spec(spec)
            # sys.modules[module_name] = module
            # spec.loader.exec_module(module)
        if invalid_modules:
            print(f"Reload scripts: {', '.join(invalid_modules.keys())}, Time: {time.time() - reload_start_time:.5f}")

    def _get_invalid_module(self):
        invalid_modules = {}
        for module_name, module in list(sys.modules.items()):
            if self._is_module_need_reload(module) and inspect.ismodule(module):
                invalid_modules[module_name] = module
        return invalid_modules

    def _is_module_need_reload(self, module):
        filename = getattr(module, '__file__', None)
        if not filename:
            return False
        if filename.endswith('.pyc') or filename.endswith('.pyo'):
            filename = filename[:-1]
        try:
            mtime = os.path.getmtime(filename)
        except OSError:
            return False
        last_mtime = self._module_mtime.get(filename, self._boot_time)
        if mtime <= last_mtime:
            return False
        self._module_mtime[filename] = mtime
        return True


def xreload(mod):
    """Reload a module in place, updating classes, methods and functions.
    
    Args:
        mod: a module object
    Returns:
        a boolean indicating whether a change was done.
    """
    r = Reload(mod)
    r.apply()
    found_change = r.found_change
    # r = None
    # pydevd_dont_trace.clear_trace_filter_cache()
    return found_change


class Reload:
    """_summary_
    
    Reload class.

    Returns:
        module: a whole py file.
        filename: file name.
        source_mtime: the last modification time about the file.
        classes: the class members in the file.
        methods: the methods members in the file.
        functions: the functions members in the file.
        found_change: a boolean to determine whether the file has changed.
    """  
    def __init__(self, module):
        self.module = module
        self.filename = module.__file__
        self.source_mtime = os.path.getmtime(self.filename)
        self.classes = self.get_classes()
        self.methods = self.get_methods()
        self.functions = self.get_functions()
        self.found_change = False

    def get_classes(self):
        classes = {}
        for name, obj in inspect.getmembers(self.module, inspect.isclass):
            classes[name] = obj
        return classes

    def get_methods(self):
        methods = {}
        for name, obj in inspect.getmembers(self.module, inspect.ismethod):
            methods[name] = obj
        return methods

    def get_functions(self):
        functions = {}
        for name, obj in inspect.getmembers(self.module, inspect.isfunction):
            functions[name] = obj
        return functions

    def apply(self):
        """_summary_
        
        check the new modication time and the origin time to determine whether refresh.
        
        """ 
        new_mtime = os.path.getmtime(self.filename)
        if new_mtime > self.source_mtime:
            logging.info("reloading module {}".format(self.module.__name__))
            new_module = xreload(self.module)
            new_classes = self.get_classes()
            new_methods = self.get_methods()
            new_functions = self.get_functions()

            for name in self.classes:
                old_class = self.classes[name]
                new_class = new_classes.get(name)
                if new_class and old_class != new_class:
                    self.found_change = True
                    logging.info("  class {} updated".format(name))
                    setattr(new_module, name, new_class)

            for name in self.methods:
                old_method = self.methods[name]
                new_method = new_methods.get(name)
                if new_method and old_method != new_method:
                    self.found_change = True
                    logging.info("  method {} updated".format(name))
                    setattr(new_module, name, new_method)

            for name in self.functions:
                old_function = self.functions[name]
                new_function = new_functions.get(name)
                if new_function and old_function != new_function:
                    self.found_change = True
                    logging.info("  function {} updated".format(name))
                    setattr(new_module, name, new_function)