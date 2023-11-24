import torch

from .create_fasterrcnn_mini_darknet_nano_head import create_fasterrcnn_mini_darknet_nano_head
from .create_fasterrcnn_mobilenet_v3_large_320_fpn import create_fasterrcnn_mobilenet_v3_large_320_fpn
from .create_fasterrcnn_mobilenet_v3_large_fpn import create_fasterrcnn_mobilenet_v3_large_fpn
from .create_fasterrcnn_resnet50_fpn_v2 import create_fasterrcnn_resnet50_fpn_v2

def load_model(model_type, path):
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        if model_type == "Mini Darknet":
            model = create_fasterrcnn_mini_darknet_nano_head().to(device)
        elif model_type == "Mobilenet_v3 large 320":
            model = create_fasterrcnn_mobilenet_v3_large_320_fpn().to(device)
        elif model_type == "Mobilenet_v3 large":
            model = create_fasterrcnn_mobilenet_v3_large_fpn().to(device)
        else:
            model = create_fasterrcnn_resnet50_fpn_v2().to(device)
        
        model.load_state_dict(torch.load(path, map_location=device))
        
        return model
    except:
        return None