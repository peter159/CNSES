# -*- coding: utf-8 -*-

import os
import sys

def make_safe_path(path: str) -> str:
    parent_path = os.path.dirname(path)
    if not os.path.exists(parent_path):
        if sys.platform.startswith("win"):
            os.system("mkdir {}".format())
        elif sys.platform.startswith("linux"):
            os.system("mkdir -p {}".format(parent_path))
    return path
