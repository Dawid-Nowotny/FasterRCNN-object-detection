from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from ..config import NUM_CLASSES

def create_fasterrcnn_resnet50_fpn_v2():
    model = fasterrcnn_resnet50_fpn_v2(
        weights=None
    )

    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, NUM_CLASSES) 

    return model