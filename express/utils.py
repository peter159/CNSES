# -*- coding: utf-8 -*-

import os


def make_file_path_if_not_exist(file_path):
    parent_path = os.path.abspath(os.path.dirname(file_path))
    os.system("mkdir -p {}".format(parent_path))
