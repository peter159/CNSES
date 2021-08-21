# -*- coding: utf-8 -*-

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
        tsne_embeded = TSNE(n_components=self.n_dimension, verbose=1).fit_transform(
            self.parent.data[self.__temp_vars__]
        )
        self.parent.data[cols] = tsne_embeded
        self.data = self.parent.data

    def show(self):
        plot_data = self.data[self.columns["tsne"]]
        color_pallette = ["red", "black", "orange", "blue", "yellow", "purple"]
        nrow = int((np.sqrt(len(self.labels)) + 0.5).round())
        fig, axs = plt.subplots(nrow, nrow)
        plt.tight_layout()      # 调整整体空白
        plt.subplots_adjust(wspace=.05, hspace=.1) # 调整子图间距
        axs = axs.ravel()
        for ax in axs:
            ax.set_xticks([])
            ax.set_yticks([])

        if self.n_dimension == 2:
            for i in range(len(self.labels)):
                values = self.data[self.labels[i]].unique()
                series = self.data[self.labels[i]]
                ax = axs[i]
                for val in values:
                    sns.scatterplot(
                        x=plot_data.iloc[:, 0][series == val],
                        y=plot_data.iloc[:, 1][series == val],
                        color=color_pallette[val - 1],
                        size=8, 
                        alpha=0.8, 
                        ax=ax
                    )
                ax.set_title(self.labels[i])
            plt.suptitle("Segment Visualization")
            plt.show()
        elif self.n_dimension == 3:
            pass
        else:
            print("n_dimension should be 2 or 3")
