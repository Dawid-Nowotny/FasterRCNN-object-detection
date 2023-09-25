import torch
from torch.optim import SGD
from torch.optim.lr_scheduler import StepLR
from tqdm import tqdm

from src.data_processing.prepare_data import prepare_data
from .validate_model import validate_model

def train(model, train_loader, val_loader, num_epochs=1, learning_rate=0.001, use_cuda=True):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.to(device)
    losses_list = []
    val_losses_list = []

    optimizer = SGD(model.parameters(), lr=learning_rate, momentum=0.9)
    lr_scheduler = StepLR(optimizer, step_size=5, gamma=0.1)

    for epoch in range(num_epochs):
        total_loss = 0.0
        train_loader = tqdm(train_loader, total=len(train_loader))

        for images, targets in train_loader:
            boxes_list, labels_list = prepare_data(targets)

            images = [img.to(device) for img in images]

            boxes_list = [boxes.to(device) for boxes in boxes_list]
            labels_list = [labels.to(device) for labels in labels_list]

            loss_dict = model(images, [{'boxes': boxes, 'labels': labels} for boxes, labels in zip(boxes_list, labels_list)])
            losses = sum(loss for loss in loss_dict.values())
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            total_loss += losses.item()

        lr_scheduler.step()

        loss = total_loss / len(train_loader)
        val_loss = validate_model(model, val_loader, device)
        losses_list.append(loss)
        val_losses_list.append(val_loss)

        print(f"Validation Loss: {val_loss}")
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss}")
    
    return model, losses_list, val_losses_list