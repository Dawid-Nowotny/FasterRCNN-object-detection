from torchvision.transforms import transforms

from src.ui.data_shelter import DataShelter

def create_transforms():
    transform_list = []
    data_shelter = DataShelter()

    transform_list.append(transforms.ToTensor())

    if data_shelter.resize:
        transform_list.append(transforms.Resize((data_shelter.resize1, data_shelter.resize2)))

    if data_shelter.horizontal_flip:
        transform_list.append(transforms.RandomHorizontalFlip())

    if data_shelter.vertical_flip:
        transform_list.append(transforms.RandomVerticalFlip())

    if data_shelter.color_jitter:
        transform_list.append(transforms.ColorJitter(
            brightness=data_shelter.brightness,
            contrast=data_shelter.contrast,
            saturation=data_shelter.saturation,
            hue=data_shelter.hue
        ))

    if data_shelter.random_rotation:
        transform_list.append(transforms.RandomRotation(data_shelter.angle))

    if data_shelter.normalize:
        transform_list.append(transforms.Normalize(
            mean=[data_shelter.mean1, data_shelter.mean2, data_shelter.mean3],
            std=[data_shelter.std1, data_shelter.std2, data_shelter.std3]
        ))

    return transforms.Compose(transform_list)
