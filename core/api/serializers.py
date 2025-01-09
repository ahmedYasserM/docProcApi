from rest_framework import serializers
from .models import UploadedImage
import base64
import uuid
from django.core.files.base import ContentFile
import binascii
from utils.file_handlers import get_image_metadata


class Base64FileField(serializers.CharField):
    def to_internal_value(self, data):
        try:
            format, file_str = data.split(";base64,")
            decoded_file = base64.b64decode(file_str)
        except (ValueError, binascii.Error):
            raise serializers.ValidationError("Invalid base64 file format.")

        if "image" in format:
            ext = format.split("/")[-1]
            file_name = f"{uuid.uuid4()}.{ext}"
        else:
            raise serializers.ValidationError(
                "Unsupported file type. Only images and PDFs are allowed."
            )

        return ContentFile(decoded_file, name=file_name)


class UploadedImageSerializer(serializers.ModelSerializer):
    file = Base64FileField(write_only=True)
    location = Base64FileField(source="file", read_only=True)

    class Meta:
        model = UploadedImage
        fields = [
            "id",
            "file",
            "location",
            "width",
            "height",
            "channels",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "width",
            "height",
            "channels",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        channels, width, height = get_image_metadata(validated_data["file"])
        validated_data["width"] = width
        validated_data["height"] = height
        validated_data["channels"] = channels

        instance = UploadedImage.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get("request").method == "POST":
            representation.pop("width", None)
            representation.pop("height", None)
            representation.pop("channels", None)

        return representation
