import cv2
import numpy as np

from src.label_colors import label_colors

def visualize_detections(image, detections):
    image_np = np.array(image)

    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    for detection in detections:
        label = detection['label']
        box = detection['bounding_box']
        score = detection['score']
        
        color = label_colors.get(label, (0, 0, 0))

        x, y, x2, y2 = map(int, box)

        label_text = f'{label} {score}'
        (_, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        
        text_window_height = text_height + 10
        
        text_x = x
        text_y = y - text_window_height if y >= text_window_height else y2 + 10
        
        cv2.rectangle(image_rgb, (x, y), (x2, y2), color, 2)
        
        cv2.putText(image_rgb, label_text, (text_x + 5, text_y + text_height + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('image', image_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()