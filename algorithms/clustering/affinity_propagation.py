# -*- coding: utf-8 -*-

from sklearn.cluster import AffinityPropagation
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from ...utils.parameters import random_seed


class AfCluster:
    def __init__(self, reader, vars) -> None:
        print("{:-^100}".format(" performing affinity propagation clustering "))
        self.parent = reader
        self.cluster_vars = vars
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        n_clusters: list of cluster
        """
        cols = ["af_labels"]
        self.parent.columns.update({"af_labels": cols})
        self.columns = self.parent.columns
        data = self.parent.data[self.cluster_vars]
        labels = AffinityPropagation(random_state=random_seed).fit(data).labels_
        self.parent.data[cols] = labels + 1
        print(
            "cluster, silhouette[-1,1]: {}, cal_har: {}".format(
                silhouette_score(data, labels),
                calinski_harabasz_score(data, labels),
            )
        )
        self.data = self.parent.data
