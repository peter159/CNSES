# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class RandomforestTyping:
    def __init__(self, cluster, vars, labels) -> None:
        print("{:-^100}".format(" start typing: Randomforest "))
        self.parent = cluster
        self.__temp_vars__ = vars
        if set(labels).issubset(self.parent.data.columns):
            self.labels = labels
        else:
            raise KeyError("keys not in data")
        self.__typing__()

    def __typing__(self):
        typing_data_x = self.parent.data[self.__temp_vars__]
        for lab in self.labels:
            typing_data_y = self.parent.data[lab].tolist()
            trainx, testx, trainy, testy = train_test_split(
                typing_data_x, typing_data_y, test_size=0.3
            )
            model = RandomForestClassifier().fit(trainx, trainy)
            trainx_predict = model.predict(trainx)
            testx_predict = model.predict(testx)
            print(
                "{} -- train prediction: {}, test prediction: {}".format(
                    lab,
                    (trainy == trainx_predict).mean(),
                    (testy == testx_predict).mean(),
                )
            )
