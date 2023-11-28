import torch
from torch.optim import SGD
from torch.optim.lr_scheduler import StepLR

from .train import train
from .validate_model import validate_model
from .test_model import test_model

def run_epochs(
        model, train_loader, val_loader, test_loader,
        num_epochs, learning_rate, momentum, weight_decay, 
        dampening, nesterov, maximize,
        step_size, gamma, iou_threshold, use_cuda
        ):

    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = SGD(model.parameters(), lr=learning_rate, momentum=momentum, dampening=dampening, weight_decay=weight_decay, nesterov=nesterov, maximize=maximize)
    lr_scheduler = StepLR(optimizer, step_size=step_size, gamma=gamma)

    losses_list = []
    val_losses_list = []
    accuracy_list = []
    val_accuracy_list = []

    for epoch in range(num_epochs):
        loss = train(model, train_loader, optimizer, device)
        val_loss = validate_model(model, val_loader, device)

        losses_list.append(loss)
        val_losses_list.append(val_loss)

        lr_scheduler.step()

        accuracy, test_mAP = test_model(model, test_loader, iou_threshold, device)
        val_accuracy, val_mAP = test_model(model, val_loader, iou_threshold, device)

        accuracy_list.append(accuracy)
        val_accuracy_list.append(val_accuracy)

        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"Validation Loss: {val_loss}")
        print(f"Loss: {loss}")
        print(f"Test Accuracy: {accuracy}")
        print(f"Validation Accuracy: {val_accuracy}")
        print(f"Test mAP: {test_mAP}")
        print(f"Validation mAP : {val_mAP}")

    return model, losses_list, val_losses_list, accuracy_list, val_accuracy_list, test_mAP, val_mAP