import torch

def save_model(model, file_path):
    try:
        torch.save(model.state_dict(), file_path)
        return True
    except:
        return False