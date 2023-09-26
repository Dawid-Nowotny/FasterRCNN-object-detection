import torch
from torch.optim import SGD
from torch.optim.lr_scheduler import StepLR

from .train import train
from .validate_model import validate_model
from .test_model import test_model

from models.save_model import save_model

from utils.plot_utils import plot_losses, plot_accuracies

def run_epochs(model, train_loader, val_loader, test_loader, num_epochs=10, learning_rate=0.001, iou_threshold=0.6, use_cuda=True):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = SGD(model.parameters(), lr=learning_rate, momentum=0.9)
    lr_scheduler = StepLR(optimizer, step_size=5, gamma=0.1)

    losses_list = []
    val_losses_list = []
    accuracy_list = []
    val_accuracy_list = []

    for epoch in range(num_epochs):
        loss = train(model, train_loader, optimizer, device=device)
        val_loss = validate_model(model, val_loader, device=device)

        losses_list.append(loss)
        val_losses_list.append(val_loss)

        lr_scheduler.step()

        accuracy = test_model(model, test_loader, use_cuda=use_cuda, iou_threshold=iou_threshold)
        val_accuracy = test_model(model, val_loader, use_cuda=use_cuda, iou_threshold=iou_threshold)

        accuracy_list.append(accuracy)
        val_accuracy_list.append(val_accuracy)

        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"Validation Loss: {val_loss}")
        print(f"Loss: {loss}")
        print(f"Test Accuracy: {accuracy}")
        print(f"Validation Accuracy: {val_accuracy}")

    save_model(model)
    plot_losses(losses_list, val_losses_list)
    plot_accuracies(accuracy_list, val_accuracy_list)