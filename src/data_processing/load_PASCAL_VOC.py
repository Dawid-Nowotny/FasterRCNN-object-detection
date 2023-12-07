from torch.utils.data import DataLoader
from torchvision.datasets import VOCDetection
import joblib

from ..config import DATA_PATH, CACHE_PATH
from .transforms import only_tensor_transform

def collate_fn(batch):
    return tuple(zip(*batch))

def load_PASCAL_VOC(year="2012", batch_size=4, data_transforms=None):
    try:
        train_dataset = joblib.load(CACHE_PATH + 'cached_data_VOC_train' + year + '.pkl')
        val_dataset = joblib.load(CACHE_PATH + 'cached_data_VOC_val' + year + '.pkl')
        test_dataset = joblib.load(CACHE_PATH + 'cached_data_VOC_test' + "2007" + '.pkl')
    except FileNotFoundError:
        train_dataset = VOCDetection(root=DATA_PATH, image_set = "train", year=year, transform=data_transforms, download=True)
        val_dataset = VOCDetection(root=DATA_PATH, image_set = "val", year=year, transform=only_tensor_transform, download=True)
        test_dataset = VOCDetection(root=DATA_PATH, image_set = "test", year="2007", transform=only_tensor_transform, download=True)
        joblib.dump(train_dataset, CACHE_PATH + 'cached_data_VOC_train' + year + '.pkl')
        joblib.dump(val_dataset, CACHE_PATH + 'cached_data_VOC_val' + year + '.pkl')
        joblib.dump(test_dataset, CACHE_PATH + 'cached_data_VOC_test' + "2007" + '.pkl')

    train_loader = DataLoader(train_dataset, batch_size=batch_size, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, collate_fn=collate_fn)

    return train_loader, val_loader, test_loader