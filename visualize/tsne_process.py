# -*- coding: utf-8 -*-

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import express
from sklearn.manifold import TSNE


class TsneVisual:
    def __init__(self, cluster, vars, labels, n_dimension=2) -> None:
        """
        cluster: cluster objects
        vars: list of vars to embedding
        labels: list of labels for plot
        n_dimension: the dimension of plot to show
        """
        self.parent = cluster
        self.__temp_vars__ = vars
        self.n_dimension = n_dimension
        self.__tsne_process__()
        if set(labels).issubset(self.data.columns):
            self.labels = labels
        else:
            raise KeyError("keys not in data")

    def __tsne_process__(self):
        cols = ["tsne_{}".format(a) for a in range(1, self.n_dimension + 1)]
        self.parent.columns.update({"tsne": cols})
        self.columns = self.parent.columns
        print("{:-^100}".format(" begin TSNE embedding "))
        tsne_embeded = TSNE(
            n_components=self.n_dimension, verbose=1, init="random", learning_rate=200
        ).fit_transform(self.parent.data[self.__temp_vars__])
        self.parent.data[cols] = tsne_embeded
        self.data = self.parent.data

    def show(self):
        nrow = int((np.sqrt(len(self.labels)) + 0.5).round())
        fig, axs = plt.subplots(nrow, nrow)
        fig.tight_layout()  # 调整整体空白
        plt.subplots_adjust(wspace=0.05, hspace=0.1)  # 调整子图间距
        axs = axs.ravel()
        for ax in axs:
            ax.set_xticks([])
            ax.set_yticks([])

        if self.n_dimension == 2:
            for i in range(len(self.labels)):
                data = self.data[["tsne_1", "tsne_2"] + [(self.labels[i])]]
                sns.scatterplot(
                    data=data,
                    x=self.data["tsne_1"],
                    y=self.data["tsne_2"],
                    hue=self.labels[i],
                    alpha=0.8,
                    palette="deep",
                    ax=axs[i],
                )
                axs[i].set_title(self.labels[i])
            plt.suptitle("Segment Visualization")
            plt.show()
        elif self.n_dimension == 3:
            for i in range(len(self.labels)):
                data = self.data[["tsne_1", "tsne_2", "tsne_3"] + [(self.labels[i])]]
                fig = express.scatter_3d(
                    data,
                    x="tsne_1",
                    y="tsne_2",
                    z="tsne_3",
                    color=self.labels[i],
                    title="cluster visualize 3D",
                )
                fig.show()
        else:
            print("n_dimension should be 2 or 3")
