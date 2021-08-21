# -*- coding: utf-8 -*-

import numpy as np


class ExponProcess:
    """
    perform exp/(exp+1)*100 process on deviation
    """

    def __init__(self, reader, vars) -> None:
        print("{:-^100}".format(" performing exp/(exp+1) transformation "))
        self.__parent__ = reader
        self.__temp_vars__ = vars
        self.__parent__.columns.update(
            {"exp": ["{}_exp".format(a) for a in self.__temp_vars__]}
        )
        self.columns = self.__parent__.columns
        self.__exp_on_vars__()
        self.data = self.__parent__.data

    def __exp_on_vars__(self):
        # row deviation
        temp_data = self.__parent__.data[self.__temp_vars__]
        temp_data = temp_data.apply(lambda x: x - x.mean(), axis=1)
        self.__parent__.data[self.columns["exp"]] = temp_data.apply(
            lambda x: (np.exp(x) / (np.exp(x) + 1)) * 100
        )

