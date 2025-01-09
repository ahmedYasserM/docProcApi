from .serializers import UploadedImageSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UploadedImage

@api_view(["POST"])
def upload_document(request):
    data = request.data
    file_data = data.get("file")

    # Determine the file type from the base64 string
    if file_data and isinstance(file_data, str):
        if file_data.startswith("data:image/"):
            serializer = UploadedImageSerializer(
                data=data, context={"request": request}
            )
        else:
            return Response(
                {"error": "Unsupported file type. Only images and PDFs are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": "Invalid file data. Expected a base64-encoded string."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate and save the file
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_images(request):
    images = UploadedImage.objects.all()
    serializer = UploadedImageSerializer(
        images, many=True, context={"request": request}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "DELETE"])
def handle_single_image(request, pk):
    try:
        image = UploadedImage.objects.get(pk=pk)
    except UploadedImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UploadedImageSerializer(
            image, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
