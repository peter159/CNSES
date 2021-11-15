# -*- coding: utf-8 -*-

from CNSES.data_process import (
    Reader,
    FaProcess,
)
from CNSES.algorithms.clustering import (
    FactorCluster,
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
        reader, vars=vars_fac1, nfactors="auto", loading_save=make_safe_path("./output/loadings.xlsx")
    )
    reader = FaProcess(
        reader, vars=vars_fac2, nfactors="auto", loading_save=make_safe_path("./output/loadings.xlsx")
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
    cluster = FactorCluster(reader, vars=vars_to_cluster)

    # typing stage
    _ = RandomforestTyping(
        cluster,
        vars=vars_fac1 + vars_fac2,
        labels=cluster.columns["fclust_labels"],
        clu_name="factorial",
    )

    # visualization stage
    visual = TsneVisual(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["fclust_labels"],
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
        clu_vars=reassign.columns["fclust_labels"], 
        outfile=make_safe_path("./raws/output/tabit_kp3-10_enlarge.xlsx"),
    )
    return reassign.data

if __name__ == "__main__":
    vars_fac1 = ['A4_1_scale', 'A4_2_scale', 'A4_3_scale', 'A4_4_scale', 'A4_5_scale',
                 'A4_6_scale', 'A4_7_scale', 'A4_8_scale', 'A4_9_scale', 'A4_10_scale',
                 'A4_11_scale', 'A4_12_scale', 'A4_13_scale', 'A4_14_scale', 'A4_15_scale',
                 'A4_16_scale', 'A4_17_scale', 'A4_18_scale']                    

    vars_fac2 = ['B1_1_scale', 'B1_2_scale', 'B1_3_scale', 'B1_4_scale', 'B1_5_scale',
                 'B1_6_scale', 'B1_7_scale', 'B1_8_scale', 'B1_9_scale', 'B1_10_scale',
                 'B1_11_scale', 'B1_12_scale', 'B1_13_scale', 'B1_14_scale', 'B1_15_scale',
                 'B1_16_scale', 'B1_17_scale', 'B1_18_scale', 'B1_19_scale', 'B1_20_scale',
                 'B1_21_scale', 'B1_22_scale', 'B1_23_scale', 'B1_24_scale', 'B1_25_scale',
                 'B1_26_scale', 'B1_27_scale', 'B1_28_scale', 'B1_29_scale', 'B1_30_scale',
                 'B1_31_scale', 'B1_32_scale', 'B1_33_scale', 'B1_34_scale', 'B1_35_scale',
                 'B1_36_scale', 'B1_37_scale', 'B1_38_scale']                    

    data = main(filepath="./data/data1113.sav")
