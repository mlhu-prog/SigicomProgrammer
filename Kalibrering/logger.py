# logger.py
from log_window import LogWindow

_log_window = None

def init_logger():
    global _log_window
    if _log_window is None:
        _log_window = LogWindow()
    return _log_window

def get_logger():
    return _log_window
