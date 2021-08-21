# -*- coding: utf-8 -*-

from sklearn.decomposition import PCA


class PcaProcess:
    def __init__(self, reader, vars) -> None:
        print("{:-^100}".format(" performing pca transformation "))
        self.__parent__ = reader
        self.__temp_vars__ = vars
        self.__pca_process__()

    def __pca_process__(self, exp_ratio=0.8):
        """
        exp_ratio: cumulative ratio threshold
        """
        nvars = len(self.__temp_vars__)
        pca = PCA(n_components=nvars).fit(self.__parent__.data[self.__temp_vars__])
        pca_ratios = pca.singular_values_ / pca.singular_values_.sum().cumsum()
        num_extract = (pca_ratios <= exp_ratio).sum()
        self.__parent__.columns.update(
            {"pca": ["{}_pca".format(a) for a in self.__temp_vars__]}
        )
        self.columns = self.__parent__.columns
        self.__parent__.data[self.columns["pca"]] = PCA(
            n_components=num_extract
        ).fit_transform(self.__parent__.data[self.__temp_vars__])
        self.data = self.__parent__.data
