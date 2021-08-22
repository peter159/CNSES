# -*- coding: utf-8 -*-

from kmodes.kprototypes import KPrototypes
from sklearn.metrics import silhouette_score, calinski_harabasz_score


class KprotoCluster:
    def __init__(self, reader, convars, catvars, nclusters) -> None:
        print("{:-^100}".format(" performing kprototypes clustering "))
        self.__parent__ = reader
        self.__temp_convars_ = convars
        self.__temp_catvars_ = catvars
        self.nclusters = nclusters
        self.__perform_clustering__()

    def __perform_clustering__(self):
        n_clusters = self.nclusters
        cols = ["kproto_{}".format(a) for a in n_clusters]
        self.__parent__.columns.update({"kproto_labels": cols})
        self.columns = self.__parent__.columns
        data = self.__parent__.data[self.__temp_convars_ + self.__temp_catvars_]
        cate_idx = [data.columns.tolist().index(x) for x in self.__temp_catvars_]
        for nc in n_clusters:
            labels = (
                KPrototypes(n_clusters=nc, verbose=0, max_iter=200)
                .fit(data, categorical=cate_idx)
                .labels_
            )
            self.__parent__.data[cols[n_clusters.index(nc)]] = labels + 1
            print(
                "cluster -- {}, silhouette[-1,1]: {}, cal_har: {}".format(
                    nc,
                    silhouette_score(data, labels),
                    calinski_harabasz_score(data, labels),
                )
            )
        self.data = self.__parent__.data
