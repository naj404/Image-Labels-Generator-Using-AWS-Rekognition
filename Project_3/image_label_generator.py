import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import io
import os

# --- Configuration Variables (MUST BE UPDATED) ---
# 1.  S3 bucket name (from AWS S3 setup)
S3_BUCKET_NAME = 'my-image-label-repo-2025'

# 2.  AWS region (from AWS S3 and IAM setup)
AWS_REGION = 'us-east-1'

# 3. The S3 key (path/filename) of the image you want to analyze
IMAGE_S3_KEY = 'images/my_test_image.jpg'

# Initialize AWS clients
# These clients use the credentials configured via 'aws configure'
s3_client = boto3.client('s3', region_name=AWS_REGION)
rekognition_client = boto3.client('rekognition', region_name=AWS_REGION)

# --- Function to detect labels using AWS Rekognition
def detect_labels_from_s3(image_s3_key, max_labels=10, min_confidence=75):
    """
    Analyzes an image stored in S3 using AWS Rekognition to detect labels.

    Args:
        image_s3_key (str): The S3 key (path/filename) of the image.
        max_labels (int): Maximum number of labels to return.
        min_confidence (int): Minimum confidence score for a label to be returned.

    Returns:
        dict: The response from Rekognition's detect_labels API call, or None if an error occurs.
    """
    print(f"Analyzing image '{image_s3_key}' from bucket '{S3_BUCKET_NAME}' with Rekognition...")
    try:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': S3_BUCKET_NAME,
                    'Name': image_s3_key
                }
            },
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        print("Label detection successful.")
        return response
    except rekognition_client.exceptions.InvalidImageFormatException:
        print("Error: The image format is not supported by Rekognition.")
    except rekognition_client.exceptions.InvalidS3ObjectException:
        print(f"Error: The S3 object '{image_s3_key}' in bucket '{S3_BUCKET_NAME}' could not be accessed or does not exist. Check bucket name, key, and permissions.")
    except Exception as e:
        print(f"An unexpected error occurred during Rekognition analysis: {e}")
    return None

# --- Function to process and display labels using Matplotlib
def process_and_display_labels_matplotlib(image_s3_key, rekognition_response):
    """
    Processes the Rekognition response and displays the image with bounding boxes
    and labels using Matplotlib.

    Args:
        image_s3_key (str): The S3 key of the processed image.
        rekognition_response (dict): The full response from detect_labels.
    """
    if not rekognition_response or not rekognition_response.get('Labels'):
        print("No labels found or invalid Rekognition response.")
        return

    # 1. Download image from S3 into memory
    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=image_s3_key)
        image_bytes = s3_object['Body'].read()
        img = Image.open(io.BytesIO(image_bytes))
        img_width, img_height = img.size
        print(f"Image '{image_s3_key}' downloaded successfully from S3.")
    except Exception as e:
        print(f"Error downloading image from S3: {e}. Check S3 bucket name, key, and permissions.")
        return

    # 2. Prepare plot for visualization
    fig, ax = plt.subplots(1)
    ax.imshow(img) # Display the image

    # 3. Extract and display labels and bounding boxes
    print("\n--- Detected Labels ---")
    for label in rekognition_response['Labels']:
        label_name = label['Name']
        confidence = round(label['Confidence'], 2)
        print(f"  - {label_name} (Confidence: {confidence}%)")

        # Check for bounding box instances (for objects)
        if 'Instances' in label:
            for instance in label['Instances']:
                if 'BoundingBox' in instance:
                    box = instance['BoundingBox']
                    # Convert normalized coordinates (0-1) to pixel coordinates
                    left = img_width * box['Left']
                    top = img_height * box['Top']
                    width = img_width * box['Width']
                    height = img_height * box['Height']

                    # Create a Rectangle patch for the bounding box
                    rect = patches.Rectangle((left, top), width, height,
                                             linewidth=2, edgecolor='r', facecolor='none')
                    ax.add_patch(rect) # Add the bounding box to the plot

                    # Add text label (Name and Confidence)
                    # Position text slightly above the top-left corner of the box
                    text_x = left
                    text_y = top - 10 if top - 10 > 0 else top + 5 # Adjust position to avoid going off top
                    ax.text(text_x, text_y, f"{label_name} ({confidence}%)",
                            fontsize=10, color='red',
                            bbox=dict(facecolor='yellow', alpha=0.6, edgecolor='none', pad=1))
        # Also display general labels (without bounding boxes) if they don't have instances
        elif 'Parents' not in label and not label.get('Instances'):
            # This is a general label for the scene, not a specific object instance
            # You might choose to display these in a separate list or on the image itself
            pass # For now, we're focusing on bounding boxes, but you can extend this

    # 4. Finalize and show plot
    ax.axis('off') # Hide axes for cleaner image display
    plt.title(f"Labels for: {os.path.basename(image_s3_key)}")
    plt.show() # Display the plot window

# --- Main execution logic
if __name__ == "__main__":
    print("Starting Image Label Generator workflow...")

    # 1. Call Rekognition to detect labels
    rekognition_response = detect_labels_from_s3(IMAGE_S3_KEY)

    # 2. Process and display the results
    if rekognition_response:
        process_and_display_labels_matplotlib(IMAGE_S3_KEY, rekognition_response)
        print("\nWorkflow completed successfully!")
    else:
        print("\nWorkflow failed due to Rekognition error. Please check messages above.")
