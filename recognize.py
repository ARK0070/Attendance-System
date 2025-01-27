import datetime
import os
import time
import cv2
import pandas as pd


def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    recognizer.read("TrainingImageLabel" + os.sep + "Trainner.yml")
    harcascadePath = "haarcascade_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    # Read the student details CSV without header, set columns manually
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv", header=None, names=['Id', 'Name'])
    
    # Print column names to verify them
    print(df.columns)  # This helps identify the column names
    
    # Handle possible whitespaces or special characters in column names
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    
    # Ensure the Id column is treated as a string type
    df['Id'] = df['Id'].astype(str)

    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Start real-time video capture
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Set width
    cam.set(4, 480)  # Set height
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,
                minSize = (int(minW), int(minH)), flags = cv2.CASCADE_SCALE_IMAGE)

        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            
            if conf < 100:
                # Look up Name based on Id
                aa = df.loc[df['Id'] == str(Id)]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id) + "-" + str(aa)
            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 67:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            tt = str(tt)[2:-2]
            if (100-conf) > 67:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5, y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100-conf) > 67:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)
            elif (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        
        if (cv2.waitKey(1) == ord('q')):
            break

    # Save attendance to CSV with timestamp
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    print("Attendance Successful")
    
    # Release resources
    cam.release()
    cv2.destroyAllWindows()
