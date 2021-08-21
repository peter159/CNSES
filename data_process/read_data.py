# -*- coding: utf-8 -*-

import pandas as pd


class Reader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data = None
        self.__readin__()

    def __readin__(self):
        print("{:-^100}".format(" readin data: " + self.file_path))
        if self.file_path.endswith(".sav"):
            self.data = pd.read_spss(self.file_path,
                                     convert_categoricals=False)
            self.columns = {"origin": self.data.columns.to_list()}

    def __repr__(self) -> str:
        if self.file_path.endswith(".sav"):
            return "<SPSS reader object>"
        return ""


