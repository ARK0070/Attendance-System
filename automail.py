import yagmail
import os

sender_email = "diodexhackathon@gmail.com"
app_password = "cueu efdn qmva drxy"  # Use your app password here

# Create a yagmail client
yag = yagmail.SMTP(user=sender_email, password=app_password)

# Email details
receiver = "receiver_email@example.com"
subject = "Your Subject"
body = "This is the body of the email."
filename = "C:\\Users\\aarya\\Smart-Attendance-System-master\\Base Papers\\attendance_report.pdf"


  # Ensure the file exists at this path

# Check if the file exists before sending the email
if not os.path.exists(filename):
    print(f"Error: The file {filename} does not exist.")
else:
    # Send email
    yag.send(
        to=receiver,
        subject=subject,
        contents=body,
        attachments=filename  # Attach the file
    )

    print("Email sent successfully!")
