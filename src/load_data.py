from torch.utils.data import DataLoader
from torchvision.datasets import VOCDetection
import joblib

from .transforms import data_transforms
from .config import DATA_PATH, CACHE_PATH, BATCH_SIZE

def collate_fn(batch):
    return tuple(zip(*batch))

def load_data(year=2008):
    try:
        train_dataset = joblib.load(CACHE_PATH + 'cached_data_' + str(year) + '.pkl')
    except FileNotFoundError:
        train_dataset = VOCDetection(root=DATA_PATH, year=str(year), transform=data_transforms, download=True)
        joblib.dump(train_dataset, CACHE_PATH + 'cached_data_' + str(year) + '.pkl')

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

    return train_loader