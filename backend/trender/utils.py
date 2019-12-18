# -*- coding: utf-8 -*-

import os

from datetime import datetime

INSTANCE_FOLDER_PATH = os.path.join(os.getcwd(), 'instance')


def get_current_time():
    return datetime.utcnow()


def make_dir(path):
    # http://stackoverflow.com/a/600612/190597 (tzot)
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
