from tqdm import tqdm

from src.data_processing.prepare_data import prepare_data

def train(model, train_loader, optimizer, device):
    model.train(True)
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

    return round(total_loss / len(train_loader), 2)