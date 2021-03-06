# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity


class ClusterReassign:
    def __init__(
        self,
        reader,
        vars,
        cluster_var,
        exclude_code,
        threshold=0.9,
        enlarge_ratio=1.3,
        balance_vars=[],
        overwrite=True,
    ) -> None:
        """
        data: pandas dataframe
        vars: list of column name
        cluster_var: str
        overwrite: whether or not to overwrite original data
        balance_vars: list of vars consider even reassign
        exclude_code: list of code in cluster_var
        """
        self.__parent__ = reader
        self.vars = vars
        self.cluster_var = cluster_var
        self.exclude_code = exclude_code
        self.threshold = threshold
        self.enlarge_ratio = enlarge_ratio
        self.overwrite = overwrite
        self.balance_vars = balance_vars
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

        if self.overwrite:
            # enlarge with ratio, and overwrite origin
            data[vars] = data[vars].apply(
                lambda x: (x - x.mean()) * self.enlarge_ratio + x.mean(), axis=1
            )
            data_x = data[vars]
        else:
            # enlarge with ratio, do not overwrite
            data_x = data[vars].apply(
                lambda x: (x - x.mean()) * self.enlarge_ratio + x.mean(), axis=1
            )
        data_x_train = data_x.iloc[remainder_idx, :]
        data_y_train = data_y[remainder_idx]
        data_x_reassign = data_x.iloc[reassign_idx, :]
        rdf_model = RandomForestClassifier().fit(data_x_train, data_y_train)
        data_y_reassign = rdf_model.predict_proba(
            data_x_reassign
        )  # (n_sample,n_classes)
        probs = pd.DataFrame(data_y_reassign)
        data_y_reassign = [
            int(rdf_model.classes_[x.argmax()]) if x.max() >= self.threshold else 999
            for x in data_y_reassign
        ]
        probs["label"] = data_y_reassign
        probs["s0c"] = self.__parent__.data[self.balance_vars]
        probs["Respondent_Serial"] = self.__parent__.data["Respondent_Serial"][
            reassign_idx
        ].to_list()
        probs.to_excel("/media/linyi/StockData/Projects/Pypkg/CNSES_test/probs.xlsx")
        reassign_name = "{}_reassign".format(cluster_var)
        self.__parent__.columns.update({"cluster_reassign": [reassign_name]})
        data[reassign_name] = data[cluster_var]
        data[reassign_name][reassign_idx] = data_y_reassign
        self.columns = self.__parent__.columns
        self.data = data
