import matplotlib.pyplot as plt

def display_example(dataset, idx):
    image, target = dataset[idx]
    objects = target['annotation']['object']
    
    plt.imshow(image.permute(1, 2, 0))
    
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
        plt.gca().add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, edgecolor='red', linewidth=2))
        plt.text(xmin, ymin - 5, label, color='red', fontsize=12, backgroundcolor='white')
    
    plt.show()