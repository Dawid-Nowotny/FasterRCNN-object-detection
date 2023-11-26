from torchvision.transforms import transforms

def create_transforms(resize, resize1, resize2,
                    horizontal_flip, vertical_flip, 
                    color_jitter, brightness, contrast, saturation, hue, 
                    random_rotation, angle, 
                    normalize, mean1, mean2, mean3, 
                    std1, std2, std3
                    ):
    
    transform_list = []

    transform_list.append(transforms.ToTensor())

    if resize:
        transform_list.append(transforms.Resize((resize1, resize2)))

    if horizontal_flip:
        transform_list.append(transforms.RandomHorizontalFlip())

    if vertical_flip:
        transform_list.append(transforms.RandomVerticalFlip())

    if color_jitter:
        transform_list.append(transforms.ColorJitter(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            hue=hue
        ))

    if random_rotation:
        transform_list.append(transforms.RandomRotation(angle))

    if normalize:
        transform_list.append(transforms.Normalize(
            mean=[mean1, mean2, mean3],
            std=[std1, std2, std3]
        ))
        
    return transforms.Compose(transform_list)
