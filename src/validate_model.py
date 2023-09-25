import torch
import torch.nn as nn
from torchvision.transforms import functional as F
from tqdm import tqdm

from src.data_processing.prepare_data import prepare_data

def validate_model(model, val_loader, use_cuda=True):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.to(device)

    total_val_loss = 0.0
    val_loader = tqdm(val_loader, total=len(val_loader))

    criterion = nn.SmoothL1Loss()

    for images, targets in val_loader:
        boxes_list, labels_list = prepare_data(targets)

        images = [img.to(device) for img in images]

        boxes_list = [boxes.to(device) for boxes in boxes_list]
        labels_list = [labels.to(device) for labels in labels_list]

        with torch.no_grad():
            loss_dict = model(images, [{'boxes': boxes, 'labels': labels} for boxes, labels in zip(boxes_list, labels_list)])
            val_losses = sum(loss for loss in loss_dict.values())
            total_val_loss += val_losses.item()

    average_val_loss = total_val_loss / len(val_loader)
    return average_val_loss