import torch.nn as nn
import torch

class BinaryClassifier(nn.Module):
    def __init__(self, num_features=468,num_classes = 2):
        super(BinaryClassifier, self).__init__()
        
        self.blockCNN = nn.Sequential(
            nn.Linear(num_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.BatchNorm1d(64),
            nn.ReLU()
        )
        
        self.classified = nn.Sequential(
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )
        
    def forward(self,x):
        branch_1 = self.blockCNN(x[:, :468])
        branch_2 = self.blockCNN(x[:, 468:])
        x = torch.cat((branch_1,branch_2),dim=1)
        x = self.classified(x)
        return x