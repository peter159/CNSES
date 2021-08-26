# -*- coding: utf-8 -*-

from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from CNSES.utils.parameters import random_seed


class SpectralCluster:
    def __init__(self, reader, vars, nclusters) -> None:
        print("{:-^100}".format(" performing spectral clustering "))
        self.parent = reader
        self.cluster_vars = vars
        self.nclusters = nclusters
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        n_clusters: list of cluster
        """
        n_clusters = self.nclusters
        cols = ["kmeans_{}".format(a) for a in n_clusters]
        self.parent.columns.update({"kmeans_labels": cols})
        self.columns = self.parent.columns
        for nc in n_clusters:
            data = self.parent.data[self.cluster_vars]
            labels = SpectralClustering(n_clusters=nc, random_state=random_seed).fit(data).labels_
            self.parent.data[cols[n_clusters.index(nc)]] = labels + 1
            print(
                "cluster -- {}, silhouette[-1,1]: {}, cal_har: {}".format(
                    nc,
                    silhouette_score(data, labels),
                    calinski_harabasz_score(data, labels),
                )
            )
        self.data = self.parent.data
