from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def index(request):

    if request.method == 'GET':
        # Logic for GET request
        courses = {
            'course_name': 'python',
            'learn': ['Flask', 'Django', 'Spring_Boot', 'FastApi'],
            'course_provider': 'GFG'
        }
        return Response(courses)

    elif request.method == 'POST':
        # Logic for POST request to accept and return JSON data
        try:
            data = request.data  # Fetch the JSON data sent in the POST request
            return Response(data, status=status.HTTP_200_OK)  # Return the same data as the response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# It sends cropped images as response

# without key dynamic label and works well

import cv2
import pytesseract
from PIL import Image
import numpy as np
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

os.environ['LD_LIBRARY_PATH'] = '/app/vendor/tesseract-ocr/lib:' + os.environ.get('LD_LIBRARY_PATH', '')


# Function to perform OCR and detect label-box pairs
def detect_label_box_pairs(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = sorted([cv2.boundingRect(c) for c in contours], key=lambda x: x[1])
    
    cropped_images = []
    for x, y, w, h in bounding_boxes:
        if w > 50 and h > 20:  # Filter small regions
            cropped = image[y:y+h, x:x+w]
            cropped_images.append(cropped)
    print(len(cropped_images))
    return cropped_images

# Convert cropped image to base64 string
def image_to_base64(cropped):
    _, buffer = cv2.imencode('.png', cropped)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

# Map cropped images to detected labels followed by colon
def map_cropped_images(cropped_images):
    image_key_map = {}
    for cropped in cropped_images:
        text = pytesseract.image_to_string(cropped).strip()
        print(text)
        # Search for label followed by colon
        if ":" in text:
            label, value = text.split(":", 1)
            label = label.strip()  # Clean the label
            image_key_map[label] = image_to_base64(cropped)  # Map the cropped image to the label
    return image_key_map

@api_view(['POST'])
def process_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    image = np.array(Image.open(image_file))

    cropped_images = detect_label_box_pairs(image)

    result = map_cropped_images(cropped_images)

    return Response(result)




import cv2
import pytesseract
from PIL import Image
import numpy as np

import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
os.environ['LD_LIBRARY_PATH'] = '/app/vendor/tesseract-ocr/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

# Function to perform OCR and detect label-box pairs
def detect_label_box_pairs(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = sorted([cv2.boundingRect(c) for c in contours], key=lambda x: x[1])
    
    cropped_images = []
    for x, y, w, h in bounding_boxes:
        if w > 50 and h > 20:  # Filter small regions
            cropped = image[y:y+h, x:x+w]
            cropped_images.append(cropped)
    print(len(cropped_images))
    return cropped_images

# Convert cropped image to base64 string
def image_to_base64(cropped):
    _, buffer = cv2.imencode('.png', cropped)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

# Map cropped images to detected labels followed by colon


@api_view(['POST'])
def list_cropped_images(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    image = np.array(Image.open(image_file))

    cropped_images = detect_label_box_pairs(image)

    count = 0

    for cropped in cropped_images:
        # text = pytesseract.image_to_string(cropped).strip()
        # print(text)
        # Search for label followed by colon
        cropped_images[count] = image_to_base64(cropped)
        count = count+1      
    return Response(cropped_images)
