import torch
import torchvision
from torch import nn
import torch.nn.functional as F
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator

from ..config import NUM_CLASSES

class TwoMLPHead(nn.Module):
    def __init__(self, in_channels, representation_size):
        super().__init__()

        self.fc6 = nn.Linear(in_channels, representation_size)
        self.fc7 = nn.Linear(representation_size, representation_size)

    def forward(self, x):
        x = x.flatten(start_dim=1)

        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))

        return x
    
class FastRCNNPredictor(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.cls_score = nn.Linear(in_channels, num_classes)
        self.bbox_pred = nn.Linear(in_channels, num_classes * 4)

    def forward(self, x):
        if x.dim() == 4:
            torch._assert(
                list(x.shape[2:]) == [1, 1],
                f"x has the wrong shape, expecting the last two dimensions to be [1,1] instead of {list(x.shape[2:])}",
            )
        x = x.flatten(start_dim=1)
        scores = self.cls_score(x)
        bbox_deltas = self.bbox_pred(x)

        return scores, bbox_deltas

class DarkNet(nn.Module):
    def __init__(self, initialize_weights=True, num_classes=20):
        super(DarkNet, self).__init__()

        self.num_classes = num_classes
        self.features = self._create_conv_layers()
        self.pool = self._pool()
        self.fcs = self._create_fc_layers()

        if initialize_weights:
            self._initialize_weights()

    def _create_conv_layers(self):
        conv_layers = nn.Sequential(
            nn.Conv2d(3, 4, 7, stride=2, padding=3),
            nn.LeakyReLU(0.1, inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(4, 8, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(8, 16, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(32, 64, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 64, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 64, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 64, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 64, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 128, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.MaxPool2d(2),

            nn.Conv2d(256, 128, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(256, 128, 1),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.LeakyReLU(0.1, inplace=True),
        )
        return conv_layers

    def _pool(self):
        pool = nn.Sequential(
            nn.AvgPool2d(7),
        )
        return pool
    
    def _create_fc_layers(self):
        fc_layers = nn.Sequential(
            nn.Linear(128, self.num_classes)
        )
        return fc_layers

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_in',
                    nonlinearity='leaky_relu'
                )
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = self.pool(x)
        x = x.squeeze()
        x = self.fcs(x)
        return x
    
def create_fasterrcnn_mini_darknet_nano_head(num_classes):
    backbone = DarkNet(num_classes=NUM_CLASSES).features

    backbone.out_channels = 128

    anchor_generator = AnchorGenerator(
        sizes=((32, 64, 128, 256, 512),),
        aspect_ratios=((0.5, 1.0, 2.0),)
    )

    roi_pooler = torchvision.ops.MultiScaleRoIAlign(
        featmap_names=['0'],
        output_size=7,
        sampling_ratio=2
    )

    representation_size = 128

    box_head = TwoMLPHead(
        in_channels=backbone.out_channels * roi_pooler.output_size[0] ** 2, 
        representation_size=representation_size
    )

    box_predictor = FastRCNNPredictor(representation_size, num_classes)

    model = FasterRCNN(
        backbone=backbone,
        num_classes=None,
        rpn_anchor_generator=anchor_generator,
        box_roi_pool=roi_pooler,
        box_head=box_head,
        box_predictor=box_predictor
    )
    
    return model