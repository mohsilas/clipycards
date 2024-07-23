import logging
from os import path
from traceback import format_exc

log_file_path = config_file_path = path.join(path.expanduser('~'), "clipycards.log")
logging.basicConfig(filename=log_file_path, level=logging.WARN, format='%(asctime)s || %(levelname)s || logger<%(name)s> || fnc<%(funcName)s()> || <msg>%(message)s</msg>')

class Debug():
    def __init__(self):
        self.version = "0.1"

    def log_err(self, module_name, e, msg="no comment"):
        logging.error("MOD: %s || %s || EXCP: %s\n<details>\n%s</details>", module_name, msg, repr(e), format_exc())
    
    def log_crit(self, module_name, e, msg="no comment"):
        logging.critical("MOD: %s || %s || EXCP: %s\n<details>\n%s</details>", module_name, msg, repr(e), format_exc())

    def log_critm(self, module_name, msg):
        logging.critical("MOD: %s || %s", module_name, msg)

    def log_warn(self, module_name, msg):
        logging.warning("MOD: %s || %s", module_name, msg)