import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from_email = "ozsuboys@gmail.com"
from_password = "June.2014"
to_email = "armanozsu@gmail.com"

message = MIMEMultipart()
message["From"] = from_email
message["To"] = to_email
message["Subject"] = "NBA Daily Digest"

body = "This is the body of the email."
message.attach(MIMEText(body, "plain"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use the appropriate SMTP server and port
    server.starttls()  # Secure the connection
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, message.as_string())
