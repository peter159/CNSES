# -*- coding: utf-8 -*-

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.metrics import silhouette_score, calinski_harabasz_score


class MeanshiftCluster:
    def __init__(self, reader, vars) -> None:
        print("{:-^100}".format(" performing mean shift clustering "))
        self.parent = reader
        self.cluster_vars = vars
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        n_clusters: list of cluster
        """
        cols = ["ms_labels"]
        self.parent.columns.update({"ms_labels": cols})
        self.columns = self.parent.columns
        data = self.parent.data[self.cluster_vars]
        bandwidth = estimate_bandwidth(data, quantile=0.1, n_samples=500) # auto detect bdwith
        labels = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data).labels_
        self.parent.data[cols] = labels + 1
        print(
            "cluster, silhouette[-1,1]: {}, cal_har: {}".format(
                silhouette_score(data, labels),
                calinski_harabasz_score(data, labels),
            )
        )
        self.data = self.parent.data
