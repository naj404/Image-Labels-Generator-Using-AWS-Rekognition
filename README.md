Image Labels Generator using AWS Rekognition
This project demonstrates a simple yet powerful application that uses AWS Rekognition to analyze images and generate labels with bounding boxes, visualizing them using Python.

Table of Contents
Features

Architecture

Technologies Used

Setup and Installation

How to Use

Project Diagram

Contributing

Features 
Analyzes images stored in an Amazon S3 bucket.

Uses AWS Rekognition's detect-labels API to identify objects and scenes.

Draws bounding boxes around detected objects.

Displays labels and confidence scores on the image.

Visualizes results using the Matplotlib library.

Architecture 
The application follows a simple cloud-based architecture:

Image Upload: An image is manually uploaded to an Amazon S3 bucket.

AWS Rekognition Analysis: A Python script uses the Boto3 SDK to call the Rekognition service, which analyzes the image in S3.

Data Processing: The Rekognition response (containing labels and bounding box coordinates) is processed by the Python script.

Visualization: The script uses Matplotlib to display the image and overlay the generated labels and bounding boxes.

Technologies Used
Python: The core programming language for the application logic.

AWS SDK for Python (Boto3): Used to interact with AWS services like S3 and Rekognition.

Amazon S3: Cloud storage for the images.

Amazon Rekognition: The core AI service for image analysis.

Matplotlib: A Python plotting library used for generating the visual output (displaying the image with labels and boxes).

Pillow (PIL): Used by Matplotlib for image handling.

Setup and Installation 
Prerequisites
An AWS account with an IAM user having permissions for s3:GetObject and rekognition:DetectLabels.

Python 3.x installed on your machine.

Step 1: Install Dependencies
Navigate to your project directory in your terminal and install the required libraries:

Bash

pip install boto3 pillow matplotlib
Step 2: AWS Configuration
Configure your AWS CLI with your IAM user credentials.

Bash

aws configure
Enter your Access Key ID, Secret Access Key, preferred AWS region (e.g., ap-southeast-1), and json as the output format.

Step 3: Create S3 Bucket and Upload Image
Create an S3 bucket in your AWS Management Console (e.g., my-image-label-repo-2025).

Upload an image to your bucket. Remember its full key (e.g., my_test_image.jpg or images/my_test_image.jpg).

How to Use 
Open the image_label_generator.py file.

Update the three configuration variables at the top of the file to match your setup:

Python

S3_BUCKET_NAME = 'YOUR_S3_BUCKET_NAME' # e.g., 'my-image-label-repo-2025'
AWS_REGION = 'YOUR_AWS_REGION' # e.g., 'ap-southeast-1'
IMAGE_S3_KEY = 'YOUR_IMAGE_S3_KEY' # e.g., 'images/my_test_image.jpg'
Save the file.

Run the script from your terminal:

Bash

python image_label_generator.py
The script will print the detected labels to the console, and a new window will pop up showing the image with bounding boxes and labels.

Project Diagram 
The project is based on the following architectural diagram:
