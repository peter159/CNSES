# -*- coding: utf-8 -*-

from sklearn.metrics import silhouette_score, calinski_harabasz_score


class FactorCluster:
    def __init__(self, reader, vars) -> None:
        print("{:-^100}".format(" performing factor clustering "))
        self.__parent__ = reader
        self.cluster_vars = vars
        self.__perform_clustering__()

    def __perform_clustering__(self):
        """
        cluster based on factor extracted
        """
        grps = list(set([x.split("_")[0] for x in self.__parent__.columns["fac"]]))
        grps.sort()
        cols = []
        for g in grps:
            var_names = [x for x in self.__parent__.columns["fac"] if x.startswith(g)]
            data = self.__parent__.data[var_names]
            labels = data.apply(lambda x: x.argmax(), axis=1)
            col_name = "fclust_{}".format(len(var_names))
            cols.append(col_name)
            self.__parent__.data[col_name] = labels + 1
            print(
                "fclust -- {}, silhouette[-1,1]: {}, cal_har: {}".format(
                    len(var_names),
                    silhouette_score(data, labels),
                    calinski_harabasz_score(data, labels),
                )
            )
            self.data = self.__parent__.data
        self.__parent__.columns.update({"fclust_labels": cols})
        self.columns = self.__parent__.columns
