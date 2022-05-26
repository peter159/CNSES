# -*- coding: utf-8 -*-

import pandas as pd
from CNSES.file_reader import Reader
from CNSES.data_process import FaProcess
from CNSES.algorithms.clustering import FactorCluster
from CNSES.tables import taball


def factor_clustering(
    data_path,
    fvar_list,
    nfac,
    tab_con_vars,
    tab_cat_vars,
    fa_output,
    tab_output,
    membership_output,
):
    """
    quick clustering
    data_path: string, file path, can be sav, xlsx, csv
    fvar_list: list, vars list use to do factor analysis
    nfac: int, number of factors to extract, default "auto"
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
    cluster = FactorCluster(reader, vars=reader.columns["fac"])
    taball(
        data=cluster.data,
        con_vars=tab_con_vars,
        cat_vars=tab_cat_vars,
        clu_vars=cluster.columns["fclust_labels"],
        outfile=tab_output,
    )
    df = pd.DataFrame(
        {
            "id": reader.data.loc[:, "SKU"].to_list(),
            "membership": reader.data.loc[
                :, cluster.columns["fclust_labels"][0]
            ].to_list(),
        }
    )
    df.to_excel(membership_output)
