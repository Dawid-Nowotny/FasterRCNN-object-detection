class DataShelter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #Transform checkoxes
            cls._instance.resize = False
            cls._instance.horizontal_flip = False
            cls._instance.vertical_flip = False
            cls._instance.color_jitter = False
            cls._instance.random_rotation = False
            cls._instance.normalize = False

            #Resize
            cls._instance.resize1 = 224
            cls._instance.resize2 = 224

            #Color Jitter
            cls._instance.brightness = 0.2
            cls._instance.contrast = 0.2
            cls._instance.saturation = 0.2
            cls._instance.hue = 0.2

            #Random rotation
            cls._instance.angle = 30

            #Normalize
            cls._instance.mean1 = 0.48
            cls._instance.mean2 = 0.45
            cls._instance.mean3 = 0.40

            cls._instance.std1 = 0.22
            cls._instance.std2 = 0.22
            cls._instance.std3 = 0.22

            #dataset
            cls._instance.chosen_year_index = 0
            cls._instance.chosen_year_text = 2008
            cls._instance.batch_size = 4


            #SGD
            cls._instance.lr = 0.001

            cls._instance.momentum = 0.0
            cls._instance.weight_decay = 0.0

            cls._instance.dampening = 0.0

            cls._instance.nesterov  = False
            cls._instance.maximize = False

            #STEPLR
            cls._instance.step_size = 5
            cls._instance.gamma = 0.1

        return cls._instance