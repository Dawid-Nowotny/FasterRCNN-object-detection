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

        return cls._instance
