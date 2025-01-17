from .serializers import UploadedImageSerializer, RotatedImageSerializer, UploadedPdfSerializer, PdfToImageSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UploadedImage, UploadedPdf
from utils.file_handlers import rotate_image, convert_pdf_to_image

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
        elif file_data.startswith("data:application/pdf"):
            serializer = UploadedPdfSerializer(
                data=data, context={"request": request})
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


@api_view(["POST"])
def rotate_image_handler(request):
    data = request.data
    serializer = RotatedImageSerializer(data=data)
    if serializer.is_valid():
        pk = serializer.validated_data["id"]
        angle = serializer.validated_data["angle"]
        try:
            image = UploadedImage.objects.get(pk=pk)
        except UploadedImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rotated_image = rotate_image(image.file.path, angle)
        return Response({"rotated_image": rotated_image}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_pdfs(request):
    pdfs = UploadedPdf.objects.all()
    serializer = UploadedPdfSerializer(
        pdfs, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "DELETE"])
def handle_single_pdf(request, pk):
    try:
        pdf = UploadedPdf.objects.get(pk=pk)
    except UploadedPdf.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UploadedPdfSerializer(pdf, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        pdf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def convert_pdf_to_image_handler(request):
    data = request.data
    serializer = PdfToImageSerializer(data=data)
    if serializer.is_valid():
        pk = serializer.validated_data["id"]
        try:
            pdf = UploadedPdf.objects.get(pk=pk)
        except UploadedPdf.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        converted_image_list = convert_pdf_to_image(pdf.file.path)
        return Response({"converted_images": converted_image_list}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
