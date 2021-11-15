# -*- coding: utf-8 -*-

import pandas as pd

# ref: https://www.datacamp.com/community/tutorials/introduction-factor-analysis
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from ..utils.parameters import random_seed


class FaProcess:
    def __init__(self, reader, vars, nfactors="auto", loading_save=None) -> None:
        print("{:-^100}".format(" performing factor analysis and transformation "))
        self.__parent__ = reader
        self.__temp_vars__ = vars
        self.nfactors = nfactors
        self.loading_save = loading_save
        self.__test_factorability__()
        self.__fa_process__()

    def __test_factorability__(self):
        data = self.__parent__.data[self.__temp_vars__]
        chi_square_val, p_val = calculate_bartlett_sphericity(data)
        _, kmo_model = calculate_kmo(data)
        print("----Test bartlett sphericity: [p value lower the better]")
        print("chi_squre_val: {}, P_val: {}".format(chi_square_val, p_val))
        print("----Test KMO: [close to 1 is better]")
        print("KMO statistics: {}".format(kmo_model))

    def __fa_process__(self):
        """
        perform factor analysis
        """
        data = self.__parent__.data[self.__temp_vars__]
        nvar = len(self.__temp_vars__)
        if self.nfactors == "auto":
            fa = FactorAnalyzer(
                n_factors=nvar, rotation="varimax", method="principal"
            ).fit(data)
            ev, _ = fa.get_eigenvalues()
            self.nfactors = (ev >= 1).sum()
        elif self.nfactors <= nvar:
            self.nfactors = int(self.nfactors)
        fa = FactorAnalyzer(
            n_factors=self.nfactors,
            rotation="varimax",
            method="principal",
        ).fit(data)
        fa_loadings = pd.DataFrame(
            fa.loadings_,
            index=data.columns,
            columns=["fac_{}".format(a) for a in range(1, self.nfactors + 1)],
        )
        fa_variance_explained = pd.DataFrame(
            fa.get_factor_variance(),
            index=["SS Loadings", "Proportion Var", "Cumulative Var"],
            columns=["fac_{}".format(a) for a in range(1, self.nfactors + 1)],
        )
        # 判断是否存在fca
        if "fac" in self.__parent__.columns.keys():
            max_fnum = [n.split("_")[0] for n in self.__parent__.columns["fac"]]
            max_fnum = max([int(x.replace("fac", "")) for x in max_fnum])
            flist = [
                "fac{}_{}".format(max_fnum + 1, a) for a in range(1, self.nfactors + 1)
            ]
            self.__parent__.columns.update(
                {"fac": self.__parent__.columns["fac"] + flist}
            )
        else:
            flist = ["fac{}_{}".format(1, a) for a in range(1, self.nfactors + 1)]
            self.__parent__.columns.update({"fac": flist})
        self.columns = self.__parent__.columns
        self.__parent__.data[flist] = fa.transform(data)
        self.data = self.__parent__.data
        if self.loading_save is not None:
            fa_loadings.to_excel(self.loading_save)
        print("----factor loading: ")
        print(fa_loadings)
        print("----factor variance explained: ")
        print(fa_variance_explained)
