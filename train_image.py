import os
import time
import cv2
import numpy as np
from PIL import Image


def getImagesAndLabels(path):
    # Ensure the folder exists
    if not os.path.exists(path):
        print(f"Folder {path} does not exist. Please create it and add images.")
        return [], []  # Return empty lists if folder doesn't exist

    # path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')  # Convert image to grayscale
        imageNp = np.array(pilImage, 'uint8')
        try:
            # Get ID from image filename (format: name.id.number.jpg)
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
        except ValueError:
            print(f"Invalid filename format for {imagePath}. Skipping this image.")
            continue  # Skip this image if ID is invalid
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrainImages():
    # Ensure the TrainingImageLabel folder exists
    if not os.path.exists("TrainingImageLabel"):
        os.makedirs("TrainingImageLabel")

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Correct function for LBPH recognizer
    harcascadePath = "haarcascade_default.xml"  # Path to Haar Cascade
    detector = cv2.CascadeClassifier(harcascadePath)  # Load Haar Cascade

    # Check if TrainingImage folder exists
    if not os.path.exists("TrainingImage"):
        print("TrainingImage folder is missing. Please create the folder and add images.")
        return

    faces, Id = getImagesAndLabels("TrainingImage")  # Get the images and IDs

    if len(faces) == 0:
        print("No valid images found in TrainingImage folder.")
        return

    # Train the recognizer with images and labels
    recognizer.train(faces, np.array(Id))

    # Start the image counter thread
    counter_img("TrainingImage")

    # Save the trained model to a file
    recognizer.save(os.path.join("TrainingImageLabel", "Trainner.yml"))
    print("Training complete. All images trained.")


def counter_img(path):
    imgcounter = 1
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    total_images = len(imagePaths)

    if total_images == 0:
        print("No images found in the folder.")
        return

    for imagePath in imagePaths:
        print(f"{imgcounter}/{total_images} Images Trained", end="\r")  # Show progress
        time.sleep(0.008)  # Small delay to simulate training process
        imgcounter += 1
    print(f"Training complete with {total_images} images.")  # Final message


# Run the training function if this script is executed
if __name__ == "__main__":
    TrainImages()
