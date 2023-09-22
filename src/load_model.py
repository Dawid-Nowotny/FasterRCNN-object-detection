import torch

from .config import MODELS_PATH

def load_model(name):
    try:
        model = torch.load(f"{MODELS_PATH}/{name}.pth")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"The model '{name}' was not found in {MODELS_PATH}")