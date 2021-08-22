# -*- coding: utf-8 -*-

import pandas as pd

class OnehotProcess:
    """
    perform onehot encoding
    """

    def __init__(self, reader, catvars) -> None:
        """
        reader: reader liked obj
        vars: list of vars to be done
        """
        print("{:-^100}".format(" performing onehot transformation "))
        self.__parent__ = reader
        self.__temp_vars__ = catvars
        self.__onehot_on_vars__()

    def __onehot_on_vars__(self):
        data = self.__parent__.data[self.__temp_vars__]
        onehot = pd.get_dummies(data, columns=self.__temp_vars__)
        cols = onehot.columns
        self.__parent__.columns.update({
            "onehot": cols.tolist()
        })
        self.columns = self.__parent__.columns
        self.__parent__.data[cols] = onehot
        self.data = self.__parent__.data
        print("generated {} of onehot variables".format(len(cols)))


