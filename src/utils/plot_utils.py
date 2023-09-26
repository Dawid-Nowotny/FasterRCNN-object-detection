import matplotlib.pyplot as plt

def plot_losses(losses, val_losses):
    epochs = range(1, len(losses) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(epochs, losses, label='Training Loss', marker='o', linestyle='-')
    plt.plot(epochs, val_losses, label='Validation Loss', marker='o', linestyle='-')

    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss Over Time')

    plt.legend()

    plt.grid(True)
    plt.show()

def plot_accuracies(accuracies, val_accuracies):
    epochs = range(1, len(accuracies) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(epochs, accuracies, label='Test Accuracy', marker='o', linestyle='-')
    plt.plot(epochs, val_accuracies, label='Validation Accuracy', marker='o', linestyle='-')

    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Test and Validation Accuracy Over Time')

    plt.legend()

    plt.grid(True)
    plt.show()