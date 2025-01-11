# DocProcAPI - Document Processing API

A powerful Django REST API for processing Images and PDFs with features like rotation, conversion, and metadata extraction.

## 🚀 Features

-  Image Upload & Management
- PDF Upload & Management
- Image Rotation
- PDF to Image Conversion
- Detailed File (image/pdf) Information

## 🛠️ Tech Stack

- Python 3.13+
- uv
- Django 5.1+
- Django REST Framework
- Pytest
- Pillow (PIL)
- PyPDF
- PDF2Image
- Docker

## 📝 API Documentation

### Image Endpoints

#### Upload Image
`POST /api/upload/`
- **Description**: Upload a new image file
- **Request Body**:
  - `file`: base64 encoded image
- **Response**: 
```json
{
    "id": image_id,
    "location": image_path_on_server,
    "created_at": created_at_timestamp,
    "updated_at": update_timestamp
}
```

#### Get all images
`GET /api/images/`
- **Description**: Retrieve all images
- **Response**: 
```json
[
    {
        "id": image1_id,
        "location": image1_path_on_server,
        "width": image1_width,
        "height": image1_height,
        "channels": image1_channels_count,
        "created_at": image1_created_at_timestamp,
        "updated_at": image1_update_timestamp
    },
    {
        "id": image2_id,
        "location": image2_path_on_server,
        "width": image2_width,
        "height": image2_height,
        "channels": image2_channels_count,
        "created_at": image2_created_at_timestamp,
        "updated_at": image2_update_timestamp
    },
    ...
]
```

#### Get Image Details
`GET /api/images/{id}/`
- **Description**: Retrieve image details by ID
- **Response**: 
```json
{
    "id": image_id,
    "location": image_path_on_server,
    "width": image_width,
    "height": image_height,
    "channels": image_channels_count,
    "created_at": created_at_timestamp,
    "updated_at": updated_at_timestamp
}

```

#### Delete Image
`DELETE /api/images/{id}/`
- **Description**: Delete an image by ID
- **Response**: Status 204 No Content

#### Rotate Image
`POST /api/images/{id}/rotate/`
- **Request Body**:
  - `id`: Image ID
  - `angle`: Rotation angle in degrees
- **Response**: 
```json
{
  "rotated_image": base64_encoded_rotated_image
}
```

### PDF Endpoints

#### Upload PDF
`POST /api/upload/`
- **Description**: Upload a new PDF file
- **Request Body**:
  - `file`: base64 encoded PDF
- **Response**:
  ```json
  {
    "id": pdf_id,
    "location": pdf_path_on_server,
    "created_at": created_at_timestamp,
    "updated_at": update_timestamp
  }
  ```

### Get all PDFs

`GET /api/pdfs/`
- **Description**: Retrieve all PDFs
- **Response**: 
```json
[
    {
        "id": pdf1_id,
        "location": pdf1_path_on_server,
        "pages": pdf1_number_of_pages,
        "page_width": pdf1_page_width,
        "page_height": pdf1_page_height,
        "created_at": pdf1_created_at_timestamp,
        "updated_at": pdf1_update_timestamp
    },
    {
        "id": pdf2_id,
        "location": pdf2_path_on_server,
        "pages": pdf2_number_of_pages,
        "page_width": pdf2_page_width,
        "page_height": pdf2_page_height,
        "created_at": pdf2_created_at_timestamp,
        "updated_at": pdf2_update_timestamp
    }
]
```
#### Get PDF Details
`GET /api/pdfs/{id}/`
- **Description**: Retrieve PDF details by ID
- **Response**: 
```json
{
    "id": pdf_id ,
    "location": pdf_path_on_server,
    "pages": number_of_pages,
    "page_width": page_width,
    "page_height": page_height,
    "created_at": created_at_timestamp,
    "updated_at": update_timestamp
}
```

#### Delete PDF
`DELETE /api/pdfs/{id}/`
- **Description**: Delete PDF by ID
- **Response**: Status 204 No Content

#### Convert to Images
`POST /api/convert-pdf-to-image/`
- **Description**: Convert PDF pages to images
- **Request Body**:
  - `id`: PDF ID
- **Response**: 
```json
{
    "converted_images": [
        "base64_encoded_image1",
        "base64_encoded_image2",
        ...
    ]
}
```

## How to Use

### Spawn a docker container directly from Docker Hub

```bash
docker run -p 8000:8000 ahmedyasserm/docprocapi
```

or 

### Build and run the docker image locally

1. Clone the repository 

```bash
git clone https://github.com/ahmedYasserM/docProcApi.git
cd docProcApi
```

2. Build docker image

```bash 
docker build -t docprocapi .
```

3. Run docker container 

```bash 
docker run -p 8000:8000 docprocapi
```
