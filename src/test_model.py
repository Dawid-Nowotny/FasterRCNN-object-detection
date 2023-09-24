import torch
from torchvision.ops import box_iou
from tqdm import tqdm

from src.data_processing.prepare_data import prepare_data

def test_model(model, train_loader, use_cuda=True, iou_threshold=0.6):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    train_loader = tqdm(train_loader, total=len(train_loader))
    
    correct = 0
    total = 0

    with torch.no_grad():
        for images, targets in train_loader:
            images = [img.to(device) for img in images]
            boxes_list, labels_list = prepare_data(targets)

            boxes_list = [boxes.to(device) for boxes in boxes_list]
            labels_list = [labels.to(device) for labels in labels_list]

            predictions = model(images)

            for i, prediction in enumerate(predictions):
                pred_boxes = prediction['boxes']
                true_boxes = boxes_list[i]

                iou = box_iou(pred_boxes, true_boxes)

                if (iou > iou_threshold).any():
                    correct += 1

                total += 1

    print(f"Accuracy: {correct / total * 100:.2f}%")