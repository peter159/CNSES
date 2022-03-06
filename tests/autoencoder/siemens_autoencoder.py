# -*- coding: utf-8 -*-

# ref: https://blog.csdn.net/weixin_33895396/article/details/112197185

import torch
import pandas as pd

from sklearn.preprocessing import StandardScaler

print("torch version:", torch.__version__)
import torchvision
import torch.nn as nn
import torch.utils.data as Data
import matplotlib.pyplot as plt

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import time

starttime = time.time()

torch.manual_seed(1)

EPOCH = 100
BATCH_SIZE = 64
LR = 0.005
N_TEST_IMG = 5

# train_data = torchvision.datasets.MNIST(
#     root="MNIST", train=True, transform=torchvision.transforms.ToTensor(), download=True
# )
##########################################################################################
from siemens_vars import con_vars, cat_vars
train_data = pd.read_spss("../data/Simens0304.sav")
stdscale = StandardScaler()
train_data = stdscale.fit_transform(train_data[con_vars])
##########################################################################################
loader = Data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)

input_var_length = len(con_vars)

class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_var_length, 128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, 16),
            nn.Tanh(),
            nn.Linear(16, 3),
        )
        self.decoder = nn.Sequential(
            nn.Linear(3, 16),
            nn.Tanh(),
            nn.Linear(16, 32),
            nn.Tanh(),
            nn.Linear(32, 64),
            nn.Tanh(),
            nn.Linear(64, 128),
            nn.Tanh(),
            nn.Linear(128, input_var_length), 
            nn.Sigmoid(),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded


coder = AutoEncoder().cuda()
print(coder)
optimizer = torch.optim.Adam(coder.parameters(), lr=LR)
loss_func = nn.MSELoss()

for epoch in range(EPOCH):
    for step, x in enumerate(loader):
        b_x = x.view(-1, input_var_length)
        encoded, decoded = coder(b_x.to(torch.float32).cuda())
        loss = loss_func(decoded.cpu(), b_x.to(torch.float32))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 5 == 0:
            print("Epoch:", epoch, "|", "train_loss:%.4f" % loss.data)

torch.save(coder.state_dict(), "AutoEncoder.pkl")
print("-------------------------------------")
print("finshed training")

view_data = torch.tensor(train_data[:]).view(-1, input_var_length).type(torch.FloatTensor)
coder.load_state_dict(torch.load("./AutoEncoder.pkl"))
encoded_data, _ = coder(view_data.cuda())
fig = plt.figure(2)
ax = Axes3D(fig)
X = encoded_data.cpu().data[:, 0].numpy()
Y = encoded_data.cpu().data[:, 1].numpy()
Z = encoded_data.cpu().data[:, 2].numpy()
# values = train_data.train_labels[:200].numpy()
values = range(view_data.shape[0])
for x, y, z, s in zip(X, Y, Z, values):
    c = cm.rainbow(int(255 * s / 9))
    ax.text(x, y, z, s, backgroundcolor=c)
ax.set_xlim(X.min(), X.max())
ax.set_ylim(Y.min(), Y.max())
ax.set_zlim(Z.min(), Z.max())
plt.show()
