# -*- coding: utf-8 -*-

from CNSES.file_reader import Reader

from CNSES.data_process import (
    ZipfProcess,
    PcaProcess,
    ExponProcess,
    FaProcess,
    OnehotProcess,
)
from CNSES.algorithms.clustering import (
    KMeansCluster,
    HcCluster,
    FactorCluster,
    KprotoCluster,
    SubspaceCluster,
    KMedoidsCluster,
)
from CNSES.visualize import TsneVisual
from CNSES.algorithms.typing import RandomforestTyping
from CNSES.tables import taball
from CNSES.utils import make_safe_path


def main(filepath: str) -> None:
    """
    perform segmentation evaluation
    """
    # preprocess stage
    reader = Reader(filepath)

    reader = FaProcess(
        reader, vars=vars_to_process, nfactors="auto", loading_save=make_safe_path("./output/loadings.xlsx")
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=5,
        loading_save=make_safe_path("./raws/output/1116A4loadings_f5.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=6,
        loading_save=make_safe_path("./raws/output/1116A4loadings_f6.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=7,
        loading_save=make_safe_path("./raws/output/1116A4loadings_f7.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=8,
        loading_save=make_safe_path("./raws/output/1116A4loadings_f8.xlsx"),
    )

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
    cluster = FactorCluster(reader, vars=vars_to_cluster)

    # typing stage
    typing = RandomforestTyping(
    cluster,
    vars=vars_to_process,
    labels=cluster.columns["fclust_labels"],
    clu_name="factorial",
    )

#     # visualization stage
#     visual = TsneVisual(
#         cluster,
#         # vars=cluster.columns["zipf"],
#         vars=vars_to_process,  # + cluster.columns["onehot"],
#         # vars=["tq423r14","tq423r15","tq423r16"],
#         # labels=cluster.columns["kmeans_labels"],
#         labels=cluster.columns["kproto_labels"],
#     )
#     visual.show()

    reassign = cluster

    # tabulation stage
    con_vars = tab_con_vars + reader.columns["fac"]
    cat_vars = tab_cat_vars
    taball(
        data=reassign.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reassign.columns["fclust_labels"], 
        outfile=make_safe_path("./raws/output/tabit.xlsx"),
    )
    return reassign.data

if __name__ == "__main__":
    import pandas as pd
    data = pd.read_excel('./data/201518401-Data-20220412.xlsx')
    df = data.drop([0])

    X1 = df.filter(like='X1').columns.tolist()
    Z0 = df.filter(like='Z0').columns.tolist()
    # df[X1+Z0]

    # con = ['J2','A6']
    # cat = ['S5','S6a','S6b','S17']

    S5 = ['S5']
    S6a = df.filter(like='S6a').columns.tolist()
    S6b = df.filter(like='S6b').columns.tolist()
    S17 = df.filter(like='S17').columns.tolist()
    J2 = df.filter(like='J2').columns.tolist()
    A6 = df.filter(like='A6').columns.tolist()
    A7 = df.filter(like='A7').columns.tolist()

    vars_to_process = X1+Z0
    tab_con_vars = X1+Z0+A6+A7
    tab_cat_vars = S5+S6a+S6b+S17+['J2_1','J2_2','J2_3']

    data = main(filepath="./data/midea_data_for_segment.sav")
    data.to_excel("./output/memership.xlsx")
