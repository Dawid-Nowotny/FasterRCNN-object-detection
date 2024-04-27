# FasterRCNN object detection
This application enables object detection in images and videos using Faster R-CNN models. It utilizes the PASCAL VOC dataset, allowing users to choose and download specific editions as needed. The application allows for dynamic data transformations, including rotation, resizing, and normalization. Users can perform training and testing on different backbones of Faster R-CNN models. They can also load and save custom models.
Object detection on loaded images and videos is supported, providing confidence values. Evaluation of training effectiveness is facilitated through graphs displaying loss, accuracy, and the mAP metric (mean Average Precision). Results, including object detection outputs and training graphs, can be saved.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
- Python 3.9 or later
- Pip
- NVIDIA GPU with CUDA support (optional): If you want to use the GPU version of the application, make sure your system has the appropriate driver and CUDA Toolkit installed compatible with your GPU version. Version 12.1 is required.

### Installing
1. Clone the repository:
    ```bash
    git clone https://github.com/Dawid-Nowotny/FasterRCNN-object-detection.git
    ```
2. (Optional) Create a virtual environment (recommended):
    ```bash
    # Windows
    python -m venv venv

    # Linux/macOS
    python3 -m venv venv
    ```

    Activate the virtual environment
    ```bash
    # Windows
    venv\Scripts\activate
    
    # Linux/macOS
    source venv/bin/activate
    ```

3. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
   ```bash
    python main.py
   ```
