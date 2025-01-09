from django.core.files.base import ContentFile
from PIL import Image
import numpy as np
import base64, io


def get_image_metadata(fileContent: ContentFile):
    """
    Returns: (channels, width, height)
    """
    img = np.array(Image.open(fileContent))
    if img.ndim == 2:
        channels = 1
    else:
        channels = img.shape[-1]
    return (channels, img.shape[1], img.shape[0])



def rotate_image(file_path, rotationAngle):
    """
    Returns: base64 string
    """
    img = Image.open(file_path)
    img = img.rotate(rotationAngle)
    img_bytes_arr = io.BytesIO()
    img.save(img_bytes_arr, format="JPEG")
    img_bytes_arr.seek(0)
    encoded_img = f"data:image/jpeg;base64,{
        base64.b64encode(img_bytes_arr.read()).decode()}"
    return encoded_img
