import csv
import cv2
import os

# Ensure the StudentDetails directory exists
if not os.path.exists("StudentDetails"):
    os.makedirs("StudentDetails")

# Check if a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

# Function to capture images
def takeImages():
    # Path to Haar Cascade classifier
    harcascadePath = "haarcascade_default.xml"  # Ensure this file is in the correct location
    cam = cv2.VideoCapture(0)

    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    # Validate ID and Name
    if(is_number(Id) and name.isalpha()):
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        # Capture images loop
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
                sampleNum = sampleNum + 1
                # Saving the captured face in the dataset folder "TrainingImage"
                cv2.imwrite("TrainingImage" + os.sep + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum >= 100:  # Stop after capturing 100 images
                break

        cam.release()
        cv2.destroyAllWindows()

        # Saving the student details in the CSV file
        res = "Images Saved for ID : " + Id + " Name : " + name
        print(res)
        row = [Id, name]  # Row containing student's ID and name
        with open("StudentDetails" + os.sep + "StudentDetails.csv", 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        if(name.isalpha()):
            print("Enter Numeric ID")

