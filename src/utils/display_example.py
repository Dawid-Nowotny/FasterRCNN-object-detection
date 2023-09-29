import matplotlib.pyplot as plt
import numpy as np
import cv2

from src.label_colors import label_colors

def display_example(dataset, idx):
    image, target = dataset[idx]
    objects = target['annotation']['object']
    
    image_np = image.permute(1, 2, 0).numpy()
    image_bgr = cv2.cvtColor((image_np * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    
    if not isinstance(objects, list):
        objects = [objects]
    
    for obj in objects:
        boxes = obj['bndbox']
        xmin, ymin, xmax, ymax = (
            int(round(float(boxes['xmin']))),
            int(round(float(boxes['ymin']))),
            int(round(float(boxes['xmax']))),
            int(round(float(boxes['ymax']))),
        )

        label = obj['name']
        color = label_colors.get(label, (0, 0, 0))
        
        cv2.rectangle(image_bgr, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(image_bgr, label, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()