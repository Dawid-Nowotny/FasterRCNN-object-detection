import torch
from torch.utils.data import DataLoader
from torchvision.datasets import VOCDetection
import joblib

from .transforms import data_transforms
from ..config import DATA_PATH, CACHE_PATH, BATCH_SIZE

def collate_fn(batch):
    return tuple(zip(*batch))

def load_data(year=2012, train_split=0.7, val_split=0.2, test_split=0.1):
    try:
        train_dataset = joblib.load(CACHE_PATH + 'cached_data_' + str(year) + '.pkl')
    except FileNotFoundError:
        train_dataset = VOCDetection(root=DATA_PATH, year=str(year), transform=data_transforms, download=True)
        joblib.dump(train_dataset, CACHE_PATH + 'cached_data_' + str(year) + '.pkl')

    num_samples = len(train_dataset)

    num_train_samples = int(train_split * num_samples)
    num_val_samples = int(val_split * num_samples)
    num_test_samples = num_samples - num_train_samples - num_val_samples

    indices = list(range(num_samples))
    train_indices = indices[:num_train_samples]
    val_indices = indices[num_train_samples:num_train_samples + num_val_samples]
    test_indices = indices[-num_test_samples:]

    train_sampler = torch.utils.data.sampler.SubsetRandomSampler(train_indices)
    val_sampler = torch.utils.data.sampler.SubsetRandomSampler(val_indices)
    test_sampler = torch.utils.data.sampler.SubsetRandomSampler(test_indices)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, sampler=train_sampler, collate_fn=collate_fn)
    val_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, sampler=val_sampler, collate_fn=collate_fn)
    test_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, sampler=test_sampler, collate_fn=collate_fn)

    return train_loader, val_loader, test_loader