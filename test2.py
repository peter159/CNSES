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
        reader, vars=vars_to_process, nfactors="auto", loading_save=make_safe_path("./output/loadings.xlsx")
    )
#     reader = FaProcess(
#         reader,
#         vars=vars_to_process,
#         nfactors=3,
#         loading_save=make_safe_path("./raws/output/loadings_f3.xlsx"),
#     )
#     reader = FaProcess(
#         reader,
#         vars=vars_to_process,
#         nfactors=4,
#         loading_save=make_safe_path("./raws/output/loadings_f4.xlsx"),
#     )
#     reader = FaProcess(
#         reader,
#         vars=vars_to_process,
#         nfactors=5,
#         loading_save=make_safe_path("./raws/output/loadings_f5.xlsx"),
#     )
#     reader = FaProcess(
#         reader,
#         vars=vars_to_process,
#         nfactors=6,
#         loading_save=make_safe_path("./raws/output/loadings_f6.xlsx"),
#     )
#     reader = FaProcess(
#         reader,
#         vars=vars_to_process,
#         nfactors=7,
#         loading_save=make_safe_path("./raws/output/loadings_f7.xlsx"),
#     )

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
#     cluster = KMeansCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6, 7])
    cluster = FactorCluster(reader, vars=vars_to_cluster)
    cluster = KprotoCluster(
        reader,
        convars=vars_to_process,
        catvars=['S7','S9'],
        nclusters=[3, 4, 5, 6, 7, 8, 9, 10],
    )

    # typing stage
#     typing = RandomforestTyping(
#         cluster,
#         vars=vars_to_process,
#         labels=cluster.columns["kmeans_labels"],
#         type="kmeans",
#     )
#     typing = RandomforestTyping(
#         cluster,
#         vars=vars_to_process,
#         labels=cluster.columns["fclust_labels"],
#         type="factorial",
#     )
    typing = RandomforestTyping(
    cluster,
    vars=vars_to_process,
    labels=cluster.columns["kproto_labels"],
    clu_name="kproto",
    )

    # visualization stage
    visual = TsneVisual(
        cluster,
        # vars=cluster.columns["zipf"],
        vars=vars_to_process,  # + cluster.columns["onehot"],
        # vars=["tq423r14","tq423r15","tq423r16"],
        # labels=cluster.columns["kmeans_labels"],
        labels=cluster.columns["kproto_labels"],
    )
    visual.show()

    reassign = cluster

    # tabulation stage
    con_vars = vars_to_process + reader.columns["fac"]
    cat_vars = ['S7','S9']
    taball(
        data=reassign.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reassign.columns["kproto_labels"], 
        outfile=make_safe_path("./raws/output/tabit_kp3-10_enlarge.xlsx"),
    )
    return reassign.data

if __name__ == "__main__":
    vars_to_process = ['A5_1', 'A5_2', 'A5_3', 'A5_4', 'A5_5', 'A5_6', 'A5_7', 'A5_8','A5b_1', 'A5b_2', 
                       'A5b_3', 'A5b_11', 'A5b_12', 'A5b_13', 'A5b_14', 'A5b_15', 'A5b_16', 'A5b_17', 
                       'A5b_21', 'A5b_22', 'A5b_23', 'A5b_24', 'A5b_25', 'A5b_26', 'A5b_27', 'A5b_31', 
                       'A5b_32', 'A5b_41', 'A5b_42', 'A5b_43', 'A5b_52', 'A5b_53', 'A5b_54', 'A5b_55', 
                       'A5b_56', 'A5b_57', 'A5b_61', 'A5b_62', 'A5b_999', 'A12_1', 'A12_2', 'A12_3', 
                       'A12_4', 'A12_5', 'A12_6', 'A12_7', 'A12_8', 'A12_9', 'A12_10', 'A12_11', 'A12_12',
                       'A12_13', 'A12_14', 'A12_15', 'A12_16', 'A12_17', 'A12_18', 'A12_19', 'A12_20', 
                       'A12_21', 'A12_22', 'A12_23', 'A12_24', 'A12_25', 'A12_26', 'A12_27', 'A12_28', 
                       'A12_29', 'A12_30', 'A12_31', 'A12_32', 'A12_33', 'A12_34', 'A12_35', 'A12_36',
                       'A12_37', 'A12_38', 'A12_39', 'A12_40', 'A12_41', 'A12_42', 'A12_43', 'A12_44', 
                       'A12_45', 'A12_46', 'A12_47', 'A12_48', 'A12_49', 'A12_50', 'A12_51','A12b_1', 
                       'A12b_2', 'A12b_3', 'A12b_4', 'A12b_5', 'A12b_6', 'A12b_7', 'A12b_8', 'A12b_9', 
                       'A12b_10', 'A12b_11', 'A12b_12', 'A12b_13', 'A12b_14', 'A12b_15', 'A12b_16', 
                       'A12b_17', 'A12b_18', 'A12b_19', 'A12b_20', 'A12b_21', 'A12b_22', 'A12b_23', 
                       'A12b_24', 'A12b_25', 'A12b_26', 'A12b_27', 'A12b_28', 'A12b_29', 'A12b_30', 
                       'A12b_31', 'A12b_32', 'A12b_33', 'A12b_34', 'A12b_35', 'A12b_36', 'A12b_37', 
                       'A12b_38', 'A12b_39', 'A12b_40', 'A12b_41', 'A12b_42', 'A12b_43', 'A12b_44', 
                       'A12b_45', 'A12b_46', 'A12b_47', 'A12b_48', 'A12b_49', 'A12b_50', 'A12b_51',
                       'B1_1_scale', 'B1_2_scale', 'B1_3_scale', 'B1_4_scale', 'B1_5_scale', 'B1_6_scale', 
                       'B1_7_scale', 'B1_8_scale', 'B1_9_scale', 'B1_10_scale', 'B1_11_scale', 'B1_12_scale',
                       'B1_13_scale', 'B1_14_scale', 'B1_15_scale', 'B1_16_scale', 'B1_17_scale', 'B1_18_scale', 
                       'B1_19_scale', 'B1_20_scale', 'B1_21_scale', 'B1_22_scale', 'B1_23_scale', 'B1_24_scale', 
                       'B1_25_scale', 'B1_26_scale', 'B1_27_scale', 'B1_28_scale', 'B1_29_scale', 'B1_30_scale', 
                       'B1_31_scale', 'B1_32_scale', 'B1_33_scale', 'B1_34_scale', 'B1_35_scale', 'B1_36_scale', 
                       'B1_37_scale', 'B1_38_scale','A3_1', 'A3_2', 'A3_3', 'A3_4', 'A3_5', 'A3_6', 'A3_7', 'A3_8', 
                       'A3_9', 'A3_10', 'A3_11', 'A3_12', 'A3_13', 'A3_14', 'A3_15', 'A3_16', 'A3_17', 'A3_18', 'A3_19', 
                       'A3_20', 'A3_21','A3_22', 'A3_23', 'A3_24','A3_25', 'A3_26', 'A3_27', 'A3_28', 'A3_999','A4_1_scale', 
                       'A4_2_scale', 'A4_3_scale', 'A4_4_scale', 'A4_5_scale','A4_6_scale', 'A4_7_scale', 'A4_8_scale', 
                       'A4_9_scale', 'A4_10_scale', 'A4_11_scale', 'A4_12_scale', 'A4_13_scale', 'A4_14_scale', 'A4_15_scale', 
                       'A4_16_scale', 'A4_17_scale', 'A4_18_scale']                    


    main(filepath="./data/data1113.sav")
#     data.to_excel("./output/table.xlsx")
