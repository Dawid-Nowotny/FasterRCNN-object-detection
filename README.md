# FasterRCNN object detection
This application enables object detection in images and videos using Faster R-CNN models. It utilizes the PASCAL VOC dataset, allowing users to choose and download specific editions as needed. The application allows for dynamic data transformations, including rotation, resizing, and normalization. Users can perform training and testing on different backbones of Faster R-CNN models. They can also load and save custom models.
Object detection on loaded images and videos is supported, providing confidence values. Evaluation of training effectiveness is facilitated through graphs displaying loss, accuracy, and the mAP metric (mean Average Precision). Results, including object detection outputs and training graphs, can be saved.


## Screenshots
| Main application view | Training results(*) |
| -------|--------------|
| <img src="https://github.com/Dawid-Nowotny/FasterRCNN-object-detection/assets/93731073/4d3822f4-1376-4fcf-ae2d-f7cd966f0d48" width="380">  | <img src="https://github.com/Dawid-Nowotny/FasterRCNN-object-detection/assets/93731073/0957928b-5433-4c6a-a0e1-2a01a7ad777c" width="380"> |

| Object detection on image | Object detection on video |
| --------------|--------------|
| <img src="https://github.com/Dawid-Nowotny/FasterRCNN-object-detection/assets/93731073/9e71bcf1-3820-45fe-ba68-442a79f614ec" width="380">  | <img src="https://github.com/Dawid-Nowotny/FasterRCNN-object-detection/assets/93731073/480c4ac2-1fda-49d4-afe0-e19b709a7079" width="380"> |

*These training results are provided for demonstration purposes only. They serve as examples to showcase the functionality of the application.

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

## Functionality
### Dataset
- Select PASCAL VOC version and download it automatically
- Save the dataset to a cache file to speed up loading in subsequent application runs
- Display an example from the dataset
- Clear the loaded dataset
- Remove saved cache files

### Model
- Load one of the Faster R-CNN models with specified backbone for training
- Load a model from a file
- Save a model
- Clear the loaded model

### Training
- Set optimizer parameters
- Set scheduler parameters
- Set training parameters
- Train the model
- Display training results

### Detection
- Recognize objects in a loaded image or video
- Replay the video
- Clear the currently displayed image or video
- Export image or video with bounding box annotations
