# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class ClusterReassign:
    def __init__(self, reader, vars, cluster_var, exclude_code) -> None:
        """
        data: pandas dataframe
        vars: list of column name
        cluster_var: str
        exclude_code: list of code in cluster_var
        """
        self.__parent__ = reader
        self.vars = vars
        self.cluster_var = cluster_var
        self.exclude_code = exclude_code
        self.cluster_reassign()

    def cluster_reassign(self):
        data = self.__parent__.data
        vars = self.vars
        cluster_var = self.cluster_var
        exclude_code = self.exclude_code
        data_y = data[cluster_var]
        reassign_idx = []
        remainder_idx = []
        count = 0
        for y in data_y:
            if y in exclude_code:
                reassign_idx.append(count)
            else:
                remainder_idx.append(count)
            count += 1
        data_x = data[vars]
        data_x_train = data_x.iloc[remainder_idx, :]
        data_y_train = data_y[remainder_idx]
        data_x_reassign = data_x.iloc[reassign_idx, :]
        rdf_model = RandomForestClassifier().fit(data_x_train, data_y_train)
        data_y_reassign = rdf_model.predict(data_x_reassign)
        reassign_name = "{}_reassign".format(cluster_var)
        self.__parent__.columns.update({
            "cluster_reassign": [reassign_name]
        })
        data[reassign_name] = data[cluster_var]
        data[reassign_name][reassign_idx] = data_y_reassign
        self.columns = self.__parent__.columns
        self.data = data
    
