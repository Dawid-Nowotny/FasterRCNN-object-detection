#Alerts
ALERT_MSG = "Wiadomość!"
ALERT_INFO = "Informacja!"
ALERT_WARNING = "Ostrzeżenie!"
ALERT_ERROR = "Bład!"
ALERT_INTERRUPTED = "Przerwano!"
ALERT_SUCCESS = "Sukces!"
ALERT_QUESTION = "Pytanie"

#Main window
MAIN_WINDOW_DETECT_IMG = "Rozpoznaj obiekty na zdjęciu"
MAIN_WINDOW_DETECT_VID = "Rozpoznaj obiekty na wideo"
CLEAR = "Wyczyść wyświetlane zdjęcie/film"
REPLAY = "Odtwórz ponownie film"
TRAINING_RESULTS = "Pokaż wyniki treningu"
MODEL_NOT_LOADED = "Model nie jest załadowany.\nNie można rozpoznać obiektów."
CHOOSE_IMG = "Wybierz obraz"
LOADING_IMG_ERROR = "Błąd podczas ładowania zdjęcia."
CHOOSE_VID = "Wybierz wideo"
LOADING_VID_ERROR = "Błąd podczas ładowania wideo."
INVALID_FILE = "Niepoprawny plik."
NON_RECOGNIZED_OBJECT_IMG = "Nie rozpoznano żadnego obiektu na zdjęciu."
NON_RECOGNIZED_OBJECT_VID = "Nie rozpoznano żadnego obiektu na całym wideo."
INTERRUPTED_DETECTION = "Detekcja obiektów została przerwana!"
DETECTION_OBJ = "Detekcja obiektów"
DETECTION_IN_PROGRESS = "Trwa detekcja..."
TIME_ALERT_LABEL = "Może to zająć do kilku do kilkunastu minut"

#Detection dialog
DETECTION_PARAMS_TITLE = "Ustaw parametry detekcji"
USE_CUDA_TITLE = "Używaj CUDA"
SCORE_TH_TITLE = "Próg wyniku"
IOU_TH_TITLE = "Próg IoU"
OPERATION_FAILED = "Nie udało się wykonac operacji"

#Training_results_dialog
TRAINING_RESULTS_TITLE = "Wyniki treningu"
MAP_TEST = "mAP na zbiorze testowym:"
MAP_VAL = "mAP na zbiorze walidacyjnym:"
MAP_50_TEST = "mAP_50 na zbiorze testowym:"
MAP_50_VAL = "mAP_50 na zbiorze walidacyjnym:"

#File_menubar
FILE_TITLE = "Plik"
SAVE_FILE_TITLE = "Zapisz aktualnie wyświetlany plik"
ICON_INFO_TITLE = "Informacje o ikonach"
ICON_SOURCE_TITLE = "Źródło ikon"
CLOSE_TITLE = "Zakończ"
NO_FILE_TO_SAVE = "Aktualnie nie wyświetla się żaden plik do zapisania."
SAVE_IMG_TITLE = "Zapisz obraz"
SAVE_VID_TITLE = "Zapisz wideo"

#dataset/dataset_menu
DATASET_MENU_TITLE = "Zbiór danych"
LOAD_DATASET_TITLE = "Wczytaj zbiór danych"
SET_TRANSFORMS_TEXT = "Ustaw transformacje"
DATASET_SAMPLE_TEXT = "Pokaż przykład ze zbioru"
CLEAR_DATASET_TEXT = "Wyczyść załadowany zbiór"
CLEAR_CACHE_TEXT = "Usuń pobrane zbiory danych"
ALREADY_LOADED_TEXT = "Zbiór danych został już załadowany!\nNie można załadować po raz kolejny!"
DATASET_LOADED_TEXT = "Zbiór danych został załadowany!"
LOADING_DATASET_INTERRUPTED_TEXT =  "Ładowanie zbioru danych zostało przerwane!"
LOADING_DATASET_TEXT = "Ładowanie zbioru danych"
LOADING_TEXT = "Trwa ładowanie..."
TIME_DATASET_TEXT = "Może to zająć od kilku do kilkunastu minut."
NONE_DATASET_TEXT = "Żaden zbiór nie jest załadowany."
CLEARED_DATASET_TEXT = "Załadowany zbiór został wyczyszczony."
QUESTION_DATASET_DEL = "Czy na pewno chcesz usunąć pobrane zbiory danych?"
CLEARD_DATASET_TEXT = "Zbiory danych został usunięte."
CLEARD_DATASET_FAILED_TEXT = "Nie udało się usunąć zbiorów!."
DATASET_NOT_LOADED_TEXT = "Zbiór danych nie jest załadowany!\nNie można wykonać tej operacji bez załadowanego zbioru!"
YES = "Tak"
NO = "Nie"

#dataset/loading_dialog
CONFIG_DS_TITLE = "Konfiguracja zbioru danych"
LOAD_DS_TITLE = "Załaduj dataset"
VOC_EDITION = "Wybierz edycję PASCAL VOC"
BATCH_TITLE = "Wybierz rozmiar batcha"

#dataset/transform_dialog
TRANSFORMS_TITLE = "Ustaw transformacje"

#model/model_dialog
MODEL_CHOOSE_TEXT = "Lista wyboru modelu"

#model/model_menu
CREATE_MODEL_TEXT = "Stwórz model Faster R-CNN"
CLEAR_MODEL_TEXT = "Wyczyść załadowany model"
LOAD_MODEL_TEXT = "Wczytaj model z pliku"
SAVE_MODEL_TEXT = "Zapisz model"
MODEL_ALREADY_LOADED_TEXT = "Model jest już załadowany."
MODEL_CREATED_TEXT =  "Model został stworzony!"
MODEL_NOT_LOADED_TEXT = "Model nie jest załadowany."
MODEL_CLEARED_TEXT = "Model został wyczyszczony."
PICK_MODEL_FILE_TEXT = "Wybierz plik modelu"
MODEL_LOADED_TEXT = "Model został załadowany."
MODEL_BACKBONE_WARN_TEXT = "Błąd podczas ładowania modelu, upewnij się,\nładujesz model Faster R-CNN z odpowiednim backbonem"
LOADING_MODEL_INTERRUPTED = "Ładowanie modelu zostało przerwane!"
MODEL_CURRENTLY_LOADING_TEXT = "Ładowanie modelu"
LOADING_MODEL_TIME_TEXT = "Może to zająć do kilku minut."
NO_MODEL_TO_SAVE = "Nie ma modelu do zapisania."
MODEL_WAS_SAVED_TEXT =  "Model został pomyślnie zapisany."
ERROR_WHILE_SAVING_MODEL_TEXT = "Błąd podczas zapisu modelu."

#training/optim_params_dialog
OPTIM_TITLE = "Ustaw parametry SGD"

#training/scheduler_params_dialog
SCHEDULER_TITLE = "Ustaw parametry STEPLR"

#training/training_menu
TRAINING_MENU_NAME = "Trening"
TRAIN_MODEL_TEXT = "Trenuj model"
OPTIM_PARAMS_TEXT = "Ustal parametry SGD"
SCHEDULER_PARAMS_TEXT = "Ustal parametry STEPLR"
CANT_START_TRANING_NO_DATASET_TEXT = "Nie można rozpocząć treningu bez załądowanych danych."
CANT_START_TRANING_NO_MODEL_TEXT = "Nie można rozpocząć treningu bez stworzonego modelu."
MODEL_TRAINED_SUCCESSFULLY = "Model został wytrenowany!"
TRAINING_INTERRUPTED = "Trening został przerwany!"
MODEL_TRANING_TEXT = "Trenowanie modelu"
MODEL_CURR_TRAINING_TEXT = "Trwa trening modelu..."
USER_PATIENCE_TEXT = "Badź cierpliwy."
TIME_TRAINING_TEXT = "Może to zająć od kilku minut do kilkunastu godzin\nw zależności od konfiguracji parametrów."

#training/training_params_dialog
DETECTION_PARAMS_TEXT = "Ustaw parametry detekcji"
EPOCH_NUM_TITLE = "Liczba epok"