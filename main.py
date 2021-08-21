# -*- coding: utf-8 -*-

from data_process import Reader, ZipfProcess, PcaProcess, ExponProcess, FaProcess
from algorithms.clustering import (
    KMeansCluster,
    AfCluster,
    MeanshiftCluster,
    SpectralCluster,
    HcCluster,
    FactorCluster,
)
from visualize import TsneVisual
from algorithms.typing import RandomforestTyping
from tables import taball
from config import con_vars, cat_vars


def main(filepath):
    """
    perform segmentation evaluation
    """
    # preprocess stage
    vars_to_process = [
        "Statistic_2",
        "Statistic_3",
        "Statistic_4",
        "Statistic_5",
        "Statistic_6",
        "Statistic_7",
        "Statistic_8",
        "Statistic_9",
        "Statistic_10",
        "Statistic_11",
        "Statistic_12",
        "Statistic_13",
        "Statistic_14",
        "Statistic_15",
        "Statistic_16",
        "Statistic_17",
        "Statistic_18",
        "Statistic_19",
        "Statistic_20",
        "Statistic_21",
        "Statistic_22",
        "Statistic_23",
        "Statistic_24",
        "Statistic_25",
        "Statistic_26",
        "Statistic_27",
        "Statistic_28",
        "Statistic_29",
        "Statistic_30",
        "Statistic_31",
        "Statistic_32",
        "Statistic_33",
        "Statistic_34",
        "Statistic_35",
        "Statistic_36",
    ]
    reader = Reader(filepath)

    reader = ZipfProcess(reader, vars=vars_to_process)
    reader = PcaProcess(reader, vars=vars_to_process)
    reader = ExponProcess(reader, vars=vars_to_process)
    # reader = FaProcess(
    #     reader, vars=vars_to_process, nfactors="auto", loading_save="./loadings.xlsx"
    # )
    reader = FaProcess(
        reader, vars=vars_to_process, nfactors=5, loading_save="./loadings.xlsx"
    )
    reader = FaProcess(
        reader, vars=vars_to_process, nfactors=6, loading_save="./loadings.xlsx"
    )
    reader = FaProcess(
        reader, vars=vars_to_process, nfactors=7, loading_save="./loadings.xlsx"
    )
    reader = FaProcess(
        reader, vars=vars_to_process, nfactors=8, loading_save="./loadings.xlsx"
    )

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
    cluster = KMeansCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    # cluster = AfCluster(reader, vars=vars_to_process)
    # cluster = MeanshiftCluster(reader, vars=vars_to_process)  # do not use it yet
    # cluster = SpectralCluster(reader, vars=vars_to_process, nclusters=[3, 4, 5, 6])
    vars_to_cluster = reader.columns["fac"]
    # cluster = HcCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    cluster = FactorCluster(reader, vars=vars_to_cluster)

    # typing stage
    typing = RandomforestTyping(
        cluster, vars=vars_to_process, labels=cluster.columns["kmeans_labels"]
    )

    # visualization stage
    visual = TsneVisual(
        cluster,
        # vars=cluster.columns["zipf"],
        vars=vars_to_process,
        # vars=["tq423r14","tq423r15","tq423r16"],
        # labels=cluster.columns["kmeans_labels"],
        labels=cluster.columns["kmeans_labels"],
    )
    visual.show()

    # tabulation stage
    taball(
        data=cluster.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reader.columns["kmeans_labels"],
        outfile="./tabit.xlsx",
    )
    return None


if __name__ == "__main__":
    # main(filepath="raws/DriverAnalysisExample.sav")
    main(filepath="./raws/maxdiff_data.sav")
