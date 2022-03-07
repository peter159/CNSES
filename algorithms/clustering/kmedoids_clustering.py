# -*- coding: utf-8 -*-

from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from ...utils.parameters import random_seed
from ...utils.dist import gower_matrix


class KMedoidsCluster:
    def __init__(
        self, reader, convars, catvars, nclusters, weight=None, precomputed=True
    ) -> None:
        print("\n{:-^90}".format(" performing kmedoids clustering "))
        self.__parent__ = reader
        self.__temp_convars_ = convars
        self.__temp_catvars_ = catvars
        self.nclusters = nclusters
        self.weight = weight
        self.precomputed = precomputed
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        n_clusters: list of cluster
        """
        n_clusters = self.nclusters
        cols = ["kmedoids_{}".format(a) for a in n_clusters]
        self.__parent__.columns.update({"kmedoids_labels": cols})
        self.columns = self.__parent__.columns

        concatvars = self.__temp_convars_ + self.__temp_catvars_
        data = self.__parent__.data[concatvars]
        for nc in n_clusters:
            if self.precomputed:
                # dist compute
                is_cat_features = [
                    True if x in self.__temp_catvars_ else False for x in concatvars
                ]
                gm = gower_matrix(
                    data.to_numpy(), weight=self.weight, is_cat_features=is_cat_features
                )
                labels = (
                    KMedoids(
                        n_clusters=nc,
                        metric="precomputed",
                        init="k-medoids++",
                        method="pam",
                        random_state=random_seed,
                    )
                    .fit(gm)
                    .labels_
                )
            else:
                raise TypeError("it has to be precomputed as the moment !")

            self.__parent__.data[cols[n_clusters.index(nc)]] = labels + 1
            print(
                "cluster -- {}, silhouette[-1,1]: {}, cal_har: {}".format(
                    nc,
                    silhouette_score(data, labels),
                    calinski_harabasz_score(data, labels),
                )
            )
        self.data = self.__parent__.data
