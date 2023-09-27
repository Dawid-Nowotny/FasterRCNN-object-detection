import torch
from torchvision.transforms import functional as F
from torchvision.ops import nms

from .label_mapping import label_mapping

def image_detect_objects(model, image, iou_threshold=0.2, score_threshold=0.6, use_cuda=True):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.eval()
    model.to(device)

    labels = {v: k for k, v in label_mapping.items()}

    image_tensor = F.to_tensor(image).to(device)

    with torch.no_grad():
        predictions = model([image_tensor])

    boxes_res = predictions[0]['boxes']
    labels_res = predictions[0]['labels']
    scores_res = predictions[0]['scores']

    selected_indices = scores_res > score_threshold
    selected_boxes = boxes_res[selected_indices]
    selected_labels = labels_res[selected_indices]
    selected_scores = scores_res[selected_indices]

    keep_indices = nms(selected_boxes, selected_scores, iou_threshold)
    selected_boxes = selected_boxes[keep_indices]
    selected_labels = selected_labels[keep_indices]
    selected_scores = selected_scores[keep_indices]

    results = []
    for box, label, score in zip(selected_boxes, selected_labels, selected_scores):
        box = [int(b) for b in box.tolist()]
        results.append({'label': labels[label.item()], 'bounding_box': box, 'score': round(float(score.item()), 2)})

    return results
