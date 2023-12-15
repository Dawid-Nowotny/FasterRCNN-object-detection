import torch
from torchvision.ops.boxes import box_iou

def non_maximum_suppression(boxes, scores, labels, iou_threshold, device):
    boxes = boxes.to(device)
    scores = scores.to(device)
    labels = labels.to(device)

    order = torch.argsort(-scores)
    keep = torch.ones(boxes.shape[0], dtype=torch.bool, device=device)

    for i in range(boxes.shape[0] - 1):
        if keep[i]:
            iou = box_iou(boxes[order[i]].unsqueeze(0), boxes[order[i + 1:]])
            suppress = i + 1 + (iou > iou_threshold).any(dim=0)
            same_class = (labels[order[i]].unsqueeze(0) == labels[order[i + 1:]])
            suppress = suppress * same_class.byte()
            keep[suppress] = False

    return order[keep]