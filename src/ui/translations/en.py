#Alerts
ALERT_MSG = "Message!"
ALERT_INFO = "Information!"
ALERT_WARNING = "Warning!"
ALERT_ERROR = "Error!"
ALERT_INTERRUPTED = "Interrupted!"
ALERT_SUCCESS = "Success!"
ALERT_QUESTION = "Question"

#Main window
MAIN_WINDOW_DETECT_IMG = "Detect Objects in Image"
MAIN_WINDOW_DETECT_VID = "Detect Objects in Video"
CLEAR = "Clear Displayed Image/Video"
REPLAY = "Replay Video"
TRAINING_RESULTS = "Show Training Results"
MODEL_NOT_LOADED = "Model not loaded.\nCannot detect objects."
CHOOSE_IMG = "Choose Image"
LOADING_IMG_ERROR = "Error loading image."
CHOOSE_VID = "Choose Video"
LOADING_VID_ERROR = "Error loading video."
INVALID_FILE = "Invalid file."
NON_RECOGNIZED_OBJECT_IMG = "No objects recognized in the image."
NON_RECOGNIZED_OBJECT_VID = "No objects recognized in the entire video."
INTERRUPTED_DETECTION = "Object detection has been interrupted!"
DETECTION_OBJ = "Object Detection"
DETECTION_IN_PROGRESS = "Detection in progress..."
TIME_ALERT_LABEL = "This may take several minutes to tens of minutes."

#Detection dialog
DETECTION_PARAMS_TITLE = "Set Detection Parameters"
USE_CUDA_TITLE = "Use CUDA"
SCORE_TH_TITLE = "Score Threshold"
IOU_TH_TITLE = "IoU Threshold"
OPERATION_FAILED = "Operation Failed"

#Training_results_dialog
TRAINING_RESULTS_TITLE = "Training Results"
MAP_TEST = "mAP on Test Set:"
MAP_VAL = "mAP on Validation Set:"
MAP_50_TEST = "mAP_50 on Test Set:"
MAP_50_VAL = "mAP_50 on Validation Set:"

#File_menubar
FILE_TITLE = "File"
SAVE_FILE_TITLE = "Save Currently Displayed File"
ICON_INFO_TITLE = "Icon Information"
ICON_SOURCE_TITLE = "Icon Source"
CLOSE_TITLE = "Close"
NO_FILE_TO_SAVE = "There is currently no file displayed to save."
SAVE_IMG_TITLE = "Save Image"
SAVE_VID_TITLE = "Save Video"

#dataset/dataset_menu
DATASET_MENU_TITLE = "Dataset"
LOAD_DATASET_TITLE = "Load Dataset"
SET_TRANSFORMS_TEXT = "Set Transforms"
DATASET_SAMPLE_TEXT = "Show Dataset Sample"
CLEAR_DATASET_TEXT = "Clear Loaded Dataset"
CLEAR_CACHE_TEXT = "Clear Cached Datasets"
ALREADY_LOADED_TEXT = "Dataset has already been loaded!\nCannot load again!"
DATASET_LOADED_TEXT = "Dataset has been loaded!"
LOADING_DATASET_INTERRUPTED_TEXT = "Loading dataset interrupted!"
LOADING_DATASET_TEXT = "Loading dataset"
LOADING_TEXT = "Loading..."
TIME_DATASET_TEXT = "This may take several minutes to tens of minutes."
NONE_DATASET_TEXT = "No dataset is currently loaded."
CLEARED_DATASET_TEXT = "Loaded dataset has been cleared."
QUESTION_DATASET_DEL = "Are you sure you want to delete cached datasets?"
CLEARD_DATASET_TEXT = "Datasets have been cleared."
CLEARD_DATASET_FAILED_TEXT = "Failed to clear datasets!"
DATASET_NOT_LOADED_TEXT = "Dataset is not loaded!\nCannot perform this operation without a loaded dataset!"
YES = "Yes"
NO = "No"

#dataset/loading_dialog
CONFIG_DS_TITLE = "Dataset Configuration"
LOAD_DS_TITLE = "Load Dataset"
VOC_EDITION = "Select PASCAL VOC Edition"
BATCH_TITLE = "Select Batch Size"

#dataset/transform_dialog
TRANSFORMS_TITLE = "Set transformations"

#model/model_dialog
MODEL_CHOOSE_TEXT = "Model selection list"

#model/model_menu
CREATE_MODEL_TEXT = "Create Faster R-CNN Model"
CLEAR_MODEL_TEXT = "Clear Loaded Model"
LOAD_MODEL_TEXT = "Load Model from File"
SAVE_MODEL_TEXT = "Save Model"
MODEL_ALREADY_LOADED_TEXT = "Model is already loaded."
MODEL_CREATED_TEXT = "Model has been created!"
MODEL_NOT_LOADED_TEXT = "Model is not loaded."
MODEL_CLEARED_TEXT = "Model has been cleared."
PICK_MODEL_FILE_TEXT = "Choose Model File"
MODEL_LOADED_TEXT = "Model has been loaded."
MODEL_BACKBONE_WARN_TEXT = "Error loading model, make sure you are\nloading a Faster R-CNN model with the correct backbone"
LOADING_MODEL_INTERRUPTED = "Loading model interrupted!"
MODEL_CURRENTLY_LOADING_TEXT = "Loading Model"
LOADING_MODEL_TIME_TEXT = "This may take a few minutes."
NO_MODEL_TO_SAVE = "No model to save."
MODEL_WAS_SAVED_TEXT = "Model was successfully saved."
ERROR_WHILE_SAVING_MODEL_TEXT = "Error while saving model."

#training/optim_params_dialog
OPTIM_TITLE = "Set SGD parameters"

#training/scheduler_params_dialog
SCHEDULER_TITLE = "Set STEPLR parameters"

#training/training_menu
TRAINING_MENU_NAME = "Training"
TRAIN_MODEL_TEXT = "Train Model"
OPTIM_PARAMS_TEXT = "Set SGD Parameters"
SCHEDULER_PARAMS_TEXT = "Set STEPLR Parameters"
CANT_START_TRANING_NO_DATASET_TEXT = "Cannot start training without loaded data."
CANT_START_TRANING_NO_MODEL_TEXT = "Cannot start training without a created model."
MODEL_TRAINED_SUCCESSFULLY = "Model has been trained!"
TRAINING_INTERRUPTED = "Training interrupted!"
MODEL_TRANING_TEXT = "Training Model"
MODEL_CURR_TRAINING_TEXT = "Model training in progress..."
USER_PATIENCE_TEXT = "Please be patient."
TIME_TRAINING_TEXT = "This may take from several minutes to several hours\ndepending on the configuration of parameters."

#training/training_params_dialog
DETECTION_PARAMS_TEXT = "Set Detection Parameters"
EPOCH_NUM_TITLE = "Number of Epochs"