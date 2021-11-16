# -*- coding: utf-8 -*-

from CNSES.data_process import (
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
from CNSES.visualize import TsneVisual
from CNSES.algorithms.typing import RandomforestTyping
from CNSES.tables import taball
from CNSES.utils import make_safe_path, ClusterReassign
from CNSES.config import vars_to_process, con_vars, cat_vars


def main(filepath: str) -> None:
    """
    perform segmentation evaluation
    """
    # preprocess stage
    reader = Reader(filepath)
    # reader = ZipfProcess(reader, vars=vars_to_process)
    # reader = PcaProcess(reader, vars=vars_to_process)
    # reader = ExponProcess(reader, vars=vars_to_process)
    reader = FaProcess(
        reader, vars=vars_to_process, nfactors="auto", loading_save="./loadings.xlsx"
    )
    # reader = FaProcess(
    #     reader,
    #     vars=vars_to_process,
    #     nfactors=5,
    #     loading_save=make_safe_path("./raws/output/loadings_f5.xlsx"),
    # )
    # reader = FaProcess(
    #     reader,
    #     vars=vars_to_process,
    #     nfactors=6,
    #     loading_save=make_safe_path("./raws/output/loadings_f6.xlsx"),
    # )
    # reader = FaProcess(
    #     reader,
    #     vars=vars_to_process,
    #     nfactors=7,
    #     loading_save=make_safe_path("./raws/output/loadings_f7.xlsx"),
    # )
    # reader = FaProcess(
    #     reader,
    #     vars=vars_to_process,
    #     nfactors=8,
    #     loading_save=make_safe_path("./raws/output/loadings_f8.xlsx"),
    # )
    # reader = OnehotProcess(reader, catvars=cat_vars)

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
    # cluster = KMeansCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    # cluster = AfCluster(reader, vars=vars_to_process)
    # cluster = MeanshiftCluster(reader, vars=vars_to_process)  # do not use it yet
    # cluster = SpectralCluster(reader, vars=vars_to_process, nclusters=[3, 4, 5, 6])
    # cluster = HcCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    # cluster = FactorCluster(reader, vars=vars_to_cluster)
    cluster = KprotoCluster(
        reader,
        convars=vars_to_process,
        catvars=["S0b", "S0c", "S4"],
        # nclusters=[3, 4, 5, 6, 7],
        nclusters=[7],
    )
    # cluster = SubpaceCluster(
    #     reader, vars=vars_to_cluster + reader.columns["onehot"], nclusters=[3, 4, 5, 6]
    # )

    # typing stage
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["kproto_labels"],
        clu_name="kproto",
    )
    # typing = RandomforestTyping(
    #     cluster,
    #     vars=vars_to_process,
    #     labels=cluster.columns["hc_labels"],
    #     type="hierarchical",
    # )
    # typing = RandomforestTyping(
    #     cluster,
    #     vars=vars_to_process,
    #     labels=cluster.columns["fclust_labels"],
    #     type="factorial",
    # )
    # typing = RandomforestTyping(
    #     cluster,
    #     vars=vars_to_process,
    #     labels=cluster.columns["subspace_labels"],
    #     type="subspace",
    # )

    # # visualization stage
    # visual = TsneVisual(
    #     cluster,
    #     # vars=cluster.columns["zipf"],
    #     vars=vars_to_process,
    #     # vars=["tq423r14","tq423r15","tq423r16"],
    #     # labels=cluster.columns["kmeans_labels"],
    #     labels=cluster.columns["kmeans_labels"],
    # )
    # visual.show()

    # reassign
    reassign = ClusterReassign(
        typing, vars=vars_to_process, cluster_var="kproto_7", exclude_code=[3], threshold=0.9
    )

    # tabulation stage
    taball(
        data=reassign.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reader.columns["kproto_labels"],
        outfile=make_safe_path("./raws/output/tabit.xlsx"),
    )
    return reassign.data


if __name__ == "__main__":
    # main(filepath="raws/DriverAnalysisExample.sav")
    data = main(filepath="./raws/maxdiff_data.sav")
