import torch
from torchvision.ops import box_iou
from tqdm import tqdm
from torchmetrics.detection import MeanAveragePrecision

from src.data_processing.prepare_data import prepare_data

def test_model(model, test_loader, iou_threshold, device):
    model.eval()
    test_loader = tqdm(test_loader, total=len(test_loader))

    correct = 0
    total = 0

    metric = MeanAveragePrecision(iou_type="bbox")

    with torch.no_grad():
        for images, targets in test_loader:
            images = [img.to(device) for img in images]
            boxes_list, labels_list = prepare_data(targets)

            boxes_list = [boxes.to(device) for boxes in boxes_list]
            labels_list = [labels.to(device) for labels in labels_list]

            predictions = model(images)

            preds = []
            target = []
            for i, prediction in enumerate(predictions):
                pred_boxes = prediction['boxes']
                true_boxes = boxes_list[i]
                pred_scores = prediction['scores']
                pred_labels = prediction['labels']

                preds.append(dict(boxes=pred_boxes, scores=pred_scores, labels=pred_labels))
                target.append(dict(boxes=true_boxes, labels=labels_list[i]))

                iou = box_iou(pred_boxes, true_boxes)

                if (iou > iou_threshold).any():
                    correct += 1

                total += 1

            metric.update(preds, target)

    mAP_result = metric.compute()

    return round(correct / total * 100, 2), mAP_result