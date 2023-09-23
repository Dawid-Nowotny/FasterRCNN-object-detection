import torch

from .create_fasterrcnn_mobilenet_v3_large_320_fpn import create_fasterrcnn_mobilenet_v3_large_320_fpn
from .config import MODELS_PATH

def load_model(name):
    try:
        if torch.cuda.is_available():
            model = create_fasterrcnn_mobilenet_v3_large_320_fpn().cuda()
            model.load_state_dict(torch.load(f"{MODELS_PATH}/{name}.pth"))
        else:
            model = create_fasterrcnn_mobilenet_v3_large_320_fpn()
            model.load_state_dict(torch.load(f"{MODELS_PATH}/{name}.pth", map_location=torch.device('cpu')))
        
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"The model '{name}' was not found in {MODELS_PATH}")
