# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from utils.parameters import random_seed


class KMeansCluster:
    def __init__(self, reader, vars, nclusters) -> None:
        print("{:-^100}".format(" performing kmeans clustering "))
        self.__parent__ = reader
        self.cluster_vars = vars
        self.nclusters = nclusters
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        n_clusters: list of cluster
        """
        n_clusters = self.nclusters
        cols = ["kmeans_{}".format(a) for a in n_clusters]
        self.__parent__.columns.update({"kmeans_labels": cols})
        self.columns = self.__parent__.columns
        for nc in n_clusters:
            data = self.__parent__.data[self.cluster_vars]
            labels = KMeans(n_clusters=nc, random_state=random_seed).fit(data).labels_
            self.__parent__.data[cols[n_clusters.index(nc)]] = labels + 1
            print(
                "cluster -- {}, silhouette[-1,1]: {}, cal_har: {}".format(
                    nc,
                    silhouette_score(data, labels),
                    calinski_harabasz_score(data, labels),
                )
            )
        self.data = self.__parent__.data
