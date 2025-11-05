# Define model
import torch
import torch.nn as nn

class VPT(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.rgb_stream = nn.Sequential(
            nn.Conv2d(3, 12, 15),
            nn.ReLU(),
            nn.Conv2d(12, 12, 7),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.ReLU()    
        )

        self.depth_stream = nn.Sequential(
            nn.Conv2d(1, 12, 15),
            nn.ReLU(),
            nn.Conv2d(12, 12, 7),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.ReLU()    
        )

        self.rnn = nn.GRU(27, 12, 1)
        self.h0 = torch.randn(1, 12)

    def forward(self, rgb, odo, depth=None):
        rgb = self.rgb_stream(rgb)
        rgb = torch.flatten(rgb, start_dim=2)
        rgb = torch.sum(rgb, dim=-1)

        depth = self.depth_stream(depth)
        depth = torch.flatten(depth, start_dim=2)
        depth = torch.sum(depth, dim=-1)

        # fuse
        slab = torch.hstack((rgb, depth, odo))

        #rnn
        out, _ = self.rnn(slab, self.h0)

        out = out.reshape((3, 4))
        delta_R = out[:, :3]
        delta_t = out[:, -1]

        return delta_R, delta_t

# Define model
class VPT_RNN(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.rgb_stream = nn.Sequential(
            nn.Conv2d(3, 12, 15),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 7),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU()        
        )

        self.depth_stream = nn.Sequential(
            nn.Conv2d(1, 12, 15),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 7),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU(),
            nn.Conv2d(12, 12, 3),
            nn.BatchNorm2d(12),
            nn.ReLU()      
        )

        self.rnn = nn.GRU(27, 12, 2)

        self.h0 = torch.randn(2, 12)

    def forward(self, rgb, odo, depth=None):
        rgb = self.rgb_stream(rgb)
        rgb = torch.flatten(rgb, start_dim=2)
        rgb = torch.sum(rgb, dim=-1)

        depth = self.depth_stream(depth)
        depth = torch.flatten(depth, start_dim=2)
        depth = torch.sum(depth, dim=-1)

        # fuse
        slab = torch.hstack((rgb, depth, odo))

        #rnn
        self.h0 = self.h0.to(device)
        out, _ = self.rnn(slab, self.h0)


        out = torch.mean(out, dim=-1)

        out = out.reshape((3, 4))
        delta_R = out[:, :3]
        delta_t = out[:, -1]

        return delta_R, delta_t