from django.core.files.base import ContentFile
from PIL import Image
import numpy as np
import base64, io
from pypdf import PdfReader
from pdf2image import convert_from_path


def get_image_metadata(file_content: ContentFile):
    """
    Returns: (channels, width, height)
    """
    img = np.array(Image.open(file_content))
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


def get_pdf_metadata(file_content: ContentFile):
    """
    Returns: (pages, width, height)
    """
    pdf_reader = PdfReader(file_content)
    mediabox = pdf_reader.pages[0].mediabox
    return (len(pdf_reader.pages), mediabox.width, mediabox.height)



def convert_pdf_to_image(filePath):
    pages = convert_from_path(filePath)
    images = []
    for page in pages:
        img_bytes_arr = io.BytesIO()
        page.save(img_bytes_arr, format="JPEG")
        img_bytes_arr.seek(0)
        encoded_img = f"data:image/jpeg;base64,{
            base64.b64encode(img_bytes_arr.read()).decode()}"
        images.append(encoded_img)

    return images
