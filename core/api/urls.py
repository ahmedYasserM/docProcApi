from django.urls import path
from .views import upload_document, get_images, handle_single_image


urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path("images/", get_images, name="get_images"),
    path("images/<int:pk>/", handle_single_image, name="handle_single_image"),
]
