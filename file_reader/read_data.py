# -*- coding: utf-8 -*-

import pandas as pd


class Reader:
    def __init__(self, file_path: str) -> None:
        """support sav, csv, excel format 2D data"""
        self.file_path = file_path
        self.sheet_name = 0
        self.__readin__()

    def __readin__(self):
        print("\n{:-^90}".format(" readin data: " + self.file_path))

        if self.file_path.endswith(".sav"):
            self.data = pd.read_spss(self.file_path, convert_categoricals=False)
        elif self.file_path.endswith(".xlsx"):
            self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        elif self.file_path.endswith(".csv"):
            self.data = pd.read_csv(self.file_path)

        self.columns = {"origin": self.data.columns.to_list()}

    def __repr__(self) -> str:
        if self.file_path.endswith(".sav"):
            return "<SPSS reader object>"
        return ""


if __name__ == "__main__":
    reader = Reader("../tests/1206vivo_data_drop_del.sav")
    # reader = Reader("../tests/data/label_siemens.xlsx")
    __import__("ipdb").set_trace()  # FIXME BREAKPOINT
