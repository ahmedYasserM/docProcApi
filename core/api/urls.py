from django.urls import path
from .views import upload_document, get_images, handle_single_image, rotate_image_handler, get_pdfs, handle_single_pdf


urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path("images/", get_images, name="get_images"),
    path("images/<int:pk>/", handle_single_image, name="handle_single_image"),
    path("rotate/", rotate_image_handler, name="rotate_image_handler"),
    path("pdfs/", get_pdfs, name="get_pdfs"),
    path("pdfs/<int:pk>/", handle_single_pdf, name="handle_single_pdf"),
]
