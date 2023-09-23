import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from src.label_colors import label_colors

def visualize_detections(image, detections):
    image_np = np.array(image)

    _, ax = plt.subplots(1, figsize=(6, 4))
    ax.imshow(image_np)

    for detection in detections:
        label = detection['label']
        box = detection['bounding_box']
        score = detection['score']
        
        color = label_colors.get(label, (0, 0, 0))
        rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        
        label_text = f'{label} {score})'
        plt.text(box[0], box[1], label_text, fontsize=8, color='white', bbox=dict(facecolor=color, alpha=0.5))
    
    plt.axis('off')
    plt.show()