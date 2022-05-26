# -*- coding: utf-8 -*-

import os
from numpy import fabs
import pandas as pd
from CNSES.file_reader import Reader
from CNSES.data_process import FaProcess
from CNSES.algorithms.clustering import FactorCluster
from CNSES.tables import taball
from CNSES.express.utils import make_file_path_if_not_exist


def factor_clustering(
    data_path,
    fvar_list,
    ncluster,
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
    ncluster: list, number of clusters to extract, default "auto"
    tab_con_vars: list, continuous vars used for tabulation
    tab_cat_vars: list, categorical vars used for tabulation
    fa_output: string, path for factor analysis output
    tab_output: string, path for tabulation output
    membership_output: string, path for membership output
    """
    # prepare and create folder
    make_file_path_if_not_exist(fa_output)
    make_file_path_if_not_exist(tab_output)
    make_file_path_if_not_exist(membership_output)

    # readin data
    reader = Reader(data_path)

    # factor analysis,always auto
    nfac = ncluster
    if ncluster != "auto":
        nfac = "auto"
    reader = FaProcess(
        reader,
        vars=fvar_list,
        nfactors=nfac,
        loading_save=fa_output,
    )
    for nc in ncluster:
        reader = FaProcess(reader, vars=fvar_list, nfactors=nc, printable=False)

    # start clustering
    cluster = FactorCluster(reader)

    # start tabulation
    if os.path.exists(tab_output):
        os.system("rm -rf {}".format(tab_output))

    taball(
        data=cluster.data,
        con_vars=tab_con_vars,
        cat_vars=tab_cat_vars,
        clu_vars=cluster.columns["fclust_labels"],
        outfile=tab_output,
    )
    df = pd.DataFrame({"id": reader.data.loc[:, "SKU"].to_list()})
    df = pd.concat(
        [
            df,
            reader.data.loc[:, cluster.columns["fclust_labels"]],
        ],
        axis=1,
    )
    df.to_excel(membership_output, index=False)
