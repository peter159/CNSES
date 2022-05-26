# -*- coding: utf-8 -*-

from CNSES.file_reader import Reader
from CNSES.data_process import FaProcess


def factor_analysis(
    data_path,
    fvar_list,
    nfac,
    fa_output,
):
    """
    factor analysis
    data_path: string, file path, can be sav, xlsx, csv
    fvar_list: list, vars list use to do factor analysis
    nfac: int, number of clusters to extract, default "auto"
    tab_con_vars: list, continuous vars used for tabulation
    tab_cat_vars: list, categorical vars used for tabulation
    fa_output: string, path for factor analysis output
    tab_output: string, path for tabulation output
    membership_output: string, path for membership output
    """
    reader = Reader(data_path)
    reader = FaProcess(
        reader,
        vars=fvar_list,
        nfactors=nfac,
        loading_save=fa_output,
    )
