import torch

from .label_mapping import label_mapping

def prepare_data(targets):
    boxes_list = []
    labels_list = []

    for target in targets:
        objects = target['annotation']['object']
        boxes = []
        labels = []

        for obj in objects:
            xmin = float(obj['bndbox']['xmin'])
            ymin = float(obj['bndbox']['ymin'])
            xmax = float(obj['bndbox']['xmax'])
            ymax = float(obj['bndbox']['ymax'])
            label = obj['name']

            label_idx = label_mapping[label]

            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(label_idx)

        boxes_list.append(torch.tensor(boxes))
        labels_list.append(torch.tensor(labels))

    return boxes_list, labels_list