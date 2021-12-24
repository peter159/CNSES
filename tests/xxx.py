# -*- coding: utf-8 -*-

import numpy as np
from kmodes.kmodes import KModes

# random categorical data
data = np.random.choice(20, (100, 10))

km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
__import__("ipdb").set_trace()  # FIXME BREAKPOINT

clusters = km.fit_predict(data)

# Print the cluster centroids
print(km.cluster_centroids_)
