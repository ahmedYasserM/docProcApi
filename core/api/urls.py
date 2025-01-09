from django.urls import path
from .views import upload_document, get_images


urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path("images/", get_images, name="get_images"),
]
