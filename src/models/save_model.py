import torch
import datetime

from ..config import MODELS_PATH

def save_model(model):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"model_{current_time}.pth"
    torch.save(model.state_dict(), MODELS_PATH + name)