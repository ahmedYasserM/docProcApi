from django.core.files.base import ContentFile
from PIL import Image
import numpy as np


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
