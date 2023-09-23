from PIL.Image import open

def load_image(image_path):
    try:
        image = open(image_path)
        return image
    except FileNotFoundError:
        raise Exception(f"File not found: {image_path}")
    except IOError as e:
        raise Exception(f"I/O error while opening the file: {image_path}. Details: {str(e)}")