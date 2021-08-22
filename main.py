# -*- coding: utf-8 -*-

from data_process import (
    Reader,
    ZipfProcess,
    PcaProcess,
    ExponProcess,
    FaProcess,
    OnehotProcess,
)
from algorithms.clustering import (
    KMeansCluster,
    AfCluster,
    MeanshiftCluster,
    SpectralCluster,
    HcCluster,
    FactorCluster,
    KprotoCluster,
    SubpaceCluster,
)
from visualize import TsneVisual
from algorithms.typing import RandomforestTyping
from tables import taball
from utils import make_safe_path
from config import vars_to_process, con_vars, cat_vars


def main(filepath: str) -> None:
    """
    perform segmentation evaluation
    """
    # preprocess stage
    reader = Reader(filepath)
    reader = ZipfProcess(reader, vars=vars_to_process)
    reader = PcaProcess(reader, vars=vars_to_process)
    reader = ExponProcess(reader, vars=vars_to_process)
    # reader = FaProcess(
    #     reader, vars=vars_to_process, nfactors="auto", loading_save="./loadings.xlsx"
    # )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=5,
        loading_save=make_safe_path("./raws/output/loadings_f5.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=6,
        loading_save=make_safe_path("./raws/output/loadings_f6.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=7,
        loading_save=make_safe_path("./raws/output/loadings_f7.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=8,
        loading_save=make_safe_path("./raws/output/loadings_f8.xlsx"),
    )
    reader = OnehotProcess(reader, catvars=cat_vars)

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
    cluster = KMeansCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    # cluster = AfCluster(reader, vars=vars_to_process)
    # cluster = MeanshiftCluster(reader, vars=vars_to_process)  # do not use it yet
    # cluster = SpectralCluster(reader, vars=vars_to_process, nclusters=[3, 4, 5, 6])
    cluster = HcCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    cluster = FactorCluster(reader, vars=vars_to_cluster)
    cluster = KprotoCluster(
        reader,
        convars=vars_to_cluster,
        catvars=["S0b", "S0c", "S4"],
        nclusters=[3, 4, 5, 6],
    )
    cluster = SubpaceCluster(
        reader, vars=vars_to_cluster + reader.columns["onehot"], nclusters=[3, 4, 5, 6]
    )

    # typing stage
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["kmeans_labels"],
        type="kmeans",
    )
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["hc_labels"],
        type="hierarchical",
    )
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["fclust_labels"],
        type="factorial",
    )
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["subspace_labels"],
        type="subspace",
    )

    # visualization stage
    visual = TsneVisual(
        cluster,
        # vars=cluster.columns["zipf"],
        vars=vars_to_process + cluster.columns["onehot"],
        # vars=["tq423r14","tq423r15","tq423r16"],
        # labels=cluster.columns["kmeans_labels"],
        labels=cluster.columns["subspace_labels"],
    )
    visual.show()

    # tabulation stage
    taball(
        data=cluster.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reader.columns["kproto_labels"],
        outfile=make_safe_path("./raws/output/tabit.xlsx"),
    )
    return None


if __name__ == "__main__":
    # main(filepath="raws/DriverAnalysisExample.sav")
    main(filepath="./raws/maxdiff_data.sav")
