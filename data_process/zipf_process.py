# -*- coding: utf-8 -*-

import pandas as pd


class ZipfProcess:
    """
    perform zipf's law
    """

    def __init__(self, reader, vars) -> None:
        """
        reader: reader liked obj
        vars: list of vars to be done
        """
        print("{:-^100}".format(" performing zipf transformation "))
        self.__parent__ = reader
        self.__temp_vars__ = vars
        self.__parent__.columns.update(
            {"zipf": ["{}_zipf".format(a) for a in self.__temp_vars__]}
        )
        self.columns = self.__parent__.columns
        self.__zipf_on_vars__()
        self.data = self.__parent__.data

    def __zipf_on_vars__(self):
        for var in self.__temp_vars__:
            var_index = self.__temp_vars__.index(var)
            self.__parent__.data[self.columns["zipf"][var_index]] = self.zipf(var)

    def zipf(self, var):
        s = self.__parent__.data[var]
        max_s = s.max()
        s_distinct = pd.Series(s.unique())
        s_distinct_rank = s_distinct.rank(ascending=False)
        rank_dict = {a: b for a, b in zip(s_distinct, s_distinct_rank)}
        return s.apply(lambda x: max_s * (1 / rank_dict[x]))
