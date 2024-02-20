import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials (replace with your own)
sender_email = "danielkioko1844@gmail.com"
password = "wxqx bnfg oqfu nmcq"

# Receiver email address
#receiver_email = "kijanadanny119@gmail.com"
receiver_email = "safariphilip89@gmail.com"

# Email content
message = MIMEMultipart("alternative")
message["Subject"] = "Project Approval"
message["From"] = sender_email
message["To"] = receiver_email


title = "Student Projects Management System"
name = "Safari Philip"
# HTML version of the message (optional)
html_content = """\
<html>
  <body>
        <p>Hello <b>{}</b> , your project tittle <b>{}</b> has been approved you can now proceed to the next milestone</p>
  </body>
</html>
""".format(name,title)

# Create a MIMEText object with the HTML content
html_part = MIMEText(html_content, "html")

#attach html part to message
message.attach(html_part)

# Connect to Gmail's SMTP server using TLS encryption
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    # Login to the server
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully!")