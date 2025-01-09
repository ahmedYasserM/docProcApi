from django.db import models
from utils.models import TrackingModel


class UploadedImage(TrackingModel):
    file = models.ImageField(upload_to="images/%y/%m/%d/",
                             default="images/default.jpg")
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    channels = models.IntegerField(default=0)
