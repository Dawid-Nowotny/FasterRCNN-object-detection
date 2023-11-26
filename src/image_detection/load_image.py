from PIL.Image import open

def load_image(image_path):
    try:
        image = open(image_path)
        return image
    except:
        return None