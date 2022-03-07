# -*- coding: utf-8 -*-

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


class RandomforestTyping:
    def __init__(self, cluster, vars, labels, clu_name) -> None:
        print("\n{:-^90}".format(" start typing: Randomforest on {} ".format(clu_name)))
        self.__parent__ = cluster
        self.__temp_vars__ = vars
        self.clu_name = clu_name
        if set(labels).issubset(self.__parent__.data.columns):
            self.labels = labels
        else:
            raise KeyError("keys not in data")
        self.__typing__()

    def __typing__(self):
        typing_data_x = self.__parent__.data[self.__temp_vars__]
        cols = [lab + "_pred" for lab in self.labels]
        self.__parent__.columns.update({self.clu_name + "predict": cols})
        self.columns = self.__parent__.columns
        for lab in self.labels:
            typing_data_y = self.__parent__.data[lab].tolist()
            trainx, testx, trainy, testy = train_test_split(
                typing_data_x, typing_data_y, test_size=0.3
            )
            model = RandomForestClassifier().fit(trainx, trainy)
            trainx_predict = model.predict(trainx)
            testx_predict = model.predict(testx)
            cm = confusion_matrix(testy, testx_predict)
            predicted_all = model.predict(typing_data_x)
            self.__parent__.data[cols[self.labels.index(lab)]] = predicted_all
            self.data = self.__parent__.data
            print(
                "{} -- train: {}, test: {}, diag: {}".format(
                    lab,
                    (trainy == trainx_predict).mean(),
                    np.round((testy == testx_predict).mean(), decimals=2),
                    (
                        np.round(
                            np.diag(
                                cm / cm.astype(np.float64).sum(axis=1).reshape([-1, 1])
                            ),
                            decimals=2,
                        )
                    ),
                )
            )
