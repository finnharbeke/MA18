import torch
import torch.nn as nn
import torch.nn.functional as F
from preprocess import preprocess
import os

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 3 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(3, 6, (32, 24))
        self.conv2 = nn.Conv2d(6, 16, (32, 24))
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(35712, 1200)
        self.fc2 = nn.Linear(1200, 150)
        self.fc3 = nn.Linear(150, 29)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

    def train(self, X, y, times, every=2000, info=False, save_path=None):

        print(X.shape) if info else None
        if save_path != None and save_path[-1] == '/':
            torch.save(self.state_dict(), save_path + "0")
            
        for epoch in range(times):

            outputs = self(X)
            print('output:', letter(outputs)) if info else None

            error = nn.MSELoss()(outputs, y)
            print('error:', float(error)) if info else None

            self.backprop(error)

            error_perImg = error.item() / X.shape[0]
            print('epoch:', epoch + 1, ',', 'error:', error_perImg/every)

            if save_path:
                if save_path[-1] == '/':
                    torch.save(self.state_dict(), save_path + str(epoch + 1))
                else:
                    torch.save(self.state_dict(), save_path)





    def backprop(self, error, learning_rate=0.01):
        self.zero_grad()
        error.backward(retain_graph=True)

        #update

        for f in self.parameters():
            f.data.sub_(f.grad.data * learning_rate)


def letter(arr):
    if arr.size()[-1] != 27:
        raise ValueError('array length gotta be 27!!')

    ind = 0
    for i in range(27):
        ind = i if arr[i] > arr[ind] else ind

    abc = [chr(i) for i in range(ord("A"), ord("Z")+1)] + [" "]
    return abc[ind]