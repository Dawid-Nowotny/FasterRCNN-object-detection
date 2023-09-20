from torch.utils.data import DataLoader
from torchvision.datasets import VOCDetection
import joblib

from .transforms import data_transforms
from .config import DATA_PATH, BATCH_SIZE

def load_data():
    try:
        train_dataset = joblib.load('cached_data.pkl')
    except FileNotFoundError:
        train_dataset = VOCDetection(root=DATA_PATH, year='2008', transform=data_transforms, download=True)
        joblib.dump(train_dataset, 'cached_data.pkl')

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    return train_loader

train_loader = load_data()
print(len(train_loader))