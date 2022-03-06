# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from CNSES.data_process import (
    Reader,
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
    SubpaceCluster,
)
from CNSES.visualize import TsneVisual
from CNSES.algorithms.typing import RandomforestTyping
from CNSES.tables import taball
from CNSES.utils import make_safe_path, ClusterReassign


def main(filepath: str) -> None:
    """
    perform segmentation evaluation
    """
    # preprocess stage
    reader = Reader(filepath)

    reader = FaProcess(
        reader, vars=vars_to_process, nfactors="auto", loading_save=make_safe_path("./output/1223combineloadings415.xlsx")
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=3,
        loading_save=make_safe_path("./output/loadingss_f3.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=4,
        loading_save=make_safe_path("./output/loadings_f4.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=5,
        loading_save=make_safe_path("./output/loadings_f5.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=6,
        loading_save=make_safe_path("./output/loadings_f6.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=7,
        loading_save=make_safe_path("./output/loadings_f7.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=8,
        loading_save=make_safe_path("./output/loadings_f8.xlsx"),
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
        outfile=make_safe_path("./output/tabit.xlsx"),
    )
    return reassign.data

if __name__ == "__main__":
    H1_Loop = ['H1_Loop_1_H1', 'H1_Loop_2_H1', 'H1_Loop_3_H1', 'H1_Loop_4_H1', 'H1_Loop_5_H1', 
            'H1_Loop_6_H1', 'H1_Loop_7_H1', 'H1_Loop_8_H1', 'H1_Loop_9_H1', 'H1_Loop_10_H1', 
            'H1_Loop_11_H1', 'H1_Loop_12_H1', 'H1_Loop_13_H1', 'H1_Loop_14_H1', 'H1_Loop_15_H1', 'H1_Loop_16_H1']
    S12C = ['S12C_Loop_1_S12C', 'S12C_Loop_2_S12C', 'S12C_Loop_3_S12C']
    A0 = ['A1_Loop_99_A1']
    A1a = ['A1_Loop_1_A1']
    A1b = ['A1_Loop_2_A1']
    A1c = ['A1_Loop_3_A1']
    A7 = ['A7_1', 'A7_2', 'A7_3', 'A7_4', 'A7_5', 'A7_6', 'A7_7', 'A7_8', 'A7_9']
    WM4_Loop_1_WM4 = ['WM4_Loop_1_WM4_1', 'WM4_Loop_1_WM4_2', 'WM4_Loop_1_WM4_3',
        'WM4_Loop_1_WM4_4', 'WM4_Loop_1_WM4_5', 'WM4_Loop_1_WM4_6',
        'WM4_Loop_1_WM4_7', 'WM4_Loop_1_WM4_8', 'WM4_Loop_1_WM4_9',
        'WM4_Loop_1_WM4_10', 'WM4_Loop_1_WM4_11', 'WM4_Loop_1_WM4_12',
        'WM4_Loop_1_WM4_13', 'WM4_Loop_1_WM4_14', 'WM4_Loop_1_WM4_15',
        'WM4_Loop_1_WM4_16', 'WM4_Loop_1_WM4_17', 'WM4_Loop_1_WM4_18',
        'WM4_Loop_1_WM4_19', 'WM4_Loop_1_WM4_20', 'WM4_Loop_1_WM4_21',
        'WM4_Loop_1_WM4_22', 'WM4_Loop_1_WM4_23', 'WM4_Loop_1_WM4_24']

    WM4_Loop_2_WM4 = ['WM4_Loop_2_WM4_1', 'WM4_Loop_2_WM4_2', 'WM4_Loop_2_WM4_3',
        'WM4_Loop_2_WM4_4', 'WM4_Loop_2_WM4_5', 'WM4_Loop_2_WM4_6',
        'WM4_Loop_2_WM4_7', 'WM4_Loop_2_WM4_8', 'WM4_Loop_2_WM4_9',
        'WM4_Loop_2_WM4_10', 'WM4_Loop_2_WM4_11', 'WM4_Loop_2_WM4_12',
        'WM4_Loop_2_WM4_13', 'WM4_Loop_2_WM4_14', 'WM4_Loop_2_WM4_15',
        'WM4_Loop_2_WM4_16', 'WM4_Loop_2_WM4_17', 'WM4_Loop_2_WM4_18',
        'WM4_Loop_2_WM4_19', 'WM4_Loop_2_WM4_20', 'WM4_Loop_2_WM4_21',
        'WM4_Loop_2_WM4_22', 'WM4_Loop_2_WM4_23', 'WM4_Loop_2_WM4_24']
    catt = ['S11A_Loop_1_S11A','S12B','S11D_Loop_1_S11D']
    conn = ['S11C_Loop_1_S11C_Num','S11C_Loop_2_S11C_Num']

    vars_to_process = H1_Loop

    tab_con_vars = H1_Loop+A7+WM4_Loop_1_WM4+WM4_Loop_2_WM4+['S11C_Loop_1_S11C_Num']
    tab_cat_vars = A0+A1a+A1b+A1c+['S11A_Loop_1_S11A','S12B','S11D_Loop_1_S11D']


    data = main(filepath="./data/Simens0304.sav")
    data.to_excel("./output/tabit_m.xlsx")
