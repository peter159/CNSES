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
    HcCluster,
    FactorCluster,
    KprotoCluster,
    SubpaceCluster,
)
from visualize import TsneVisual
from algorithms.typing import RandomforestTyping
from tables import taball
from utils import make_safe_path


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
        reader, vars=vars_to_process, nfactors="auto", loading_save=make_safe_path("./raws/output/loadings.xlsx")
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=3,
        loading_save=make_safe_path("./raws/output/loadings_f3.xlsx"),
    )
    reader = FaProcess(
        reader,
        vars=vars_to_process,
        nfactors=4,
        loading_save=make_safe_path("./raws/output/loadings_f4.xlsx"),
    )
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
    # reader = OnehotProcess(reader, catvars=cat_vars)

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
#     cluster = KMeansCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6, 7])
#     cluster = HcCluster(reader, vars=vars_to_cluster, nclusters=[3, 4, 5, 6])
    cluster = FactorCluster(reader, vars=vars_to_cluster)
#     cluster = KprotoCluster(
#         reader,
#         convars=vars_to_cluster,
#         catvars=["S0b", "S0c", "S4"],
#         nclusters=[3, 4, 5, 6],
#     )
#     cluster = SubpaceCluster(
#         reader, vars=vars_to_cluster + reader.columns["onehot"], nclusters=[3, 4, 5, 6]
#     )

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
#         labels=cluster.columns["hc_labels"],
#         type="hierarchical",
#     )
    typing = RandomforestTyping(
        cluster,
        vars=vars_to_process,
        labels=cluster.columns["fclust_labels"],
        type="factorial",
    )
#     typing = RandomforestTyping(
#         cluster,
#         vars=vars_to_process,
#         labels=cluster.columns["subspace_labels"],
#         type="subspace",
#     )

    # visualization stage
    visual = TsneVisual(
        cluster,
        # vars=cluster.columns["zipf"],
        vars=vars_to_process,  # + cluster.columns["onehot"],
        # vars=["tq423r14","tq423r15","tq423r16"],
        # labels=cluster.columns["kmeans_labels"],
        labels=cluster.columns["fclust_labels"],
    )
    visual.show()
    
    con_vars = vars_to_process + ['S3'] + reader.columns["fac"]
    cat_vars = ['S0c','S4','A5','A6']
    # tabulation stage
    taball(
        data=cluster.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=reader.columns["fclust_labels"],
        outfile=make_safe_path("./raws/output/tabit2.xlsx"),
    )
    return None


if __name__ == "__main__":
    vars_to_process = ['Statistic_2','Statistic_3','Statistic_4','Statistic_5','Statistic_6','Statistic_7',
               'Statistic_8','Statistic_9','Statistic_10','Statistic_11','Statistic_12','Statistic_13','Statistic_14',
               'Statistic_15','Statistic_16','Statistic_17','Statistic_18','Statistic_19','Statistic_20','Statistic_21',
               'Statistic_22','Statistic_23','Statistic_24','Statistic_25','Statistic_26','Statistic_27','Statistic_28',
               'Statistic_29','Statistic_30','Statistic_31','Statistic_32','Statistic_33','Statistic_34','Statistic_35',
               'Statistic_36']                    

    main(filepath="raws/maxdiff_data.sav")
