import serial
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
s = serial.Serial('/dev/ttyACM0', 9600)
started = False

def printgpx(gpsdata):
    gpxcontent = '<?xml version="1.0" encoding="UTF-8"?>\n\
<gpx version="1.0">\n\
    <name>Example gpx</name>\n\
        <trk>\n\
            <name>Example gpx</name><number>1</number>\n\
                <trkseg>\n'
    for point in gpsdata:
        gpxcontent += '\
                    <trkpt lat="'+point[0]+'" lon="'+point[1]+'"><ele>0</ele><time>2007-10-14T10:09:57Z</time></trkpt>\n'
    gpxcontent += '\
                </trkseg>\n\
        </trk>\n\
</gpx>'
    text_file = open("Output.gpx", "w")
    text_file.write(gpxcontent)
    text_file.close()


def sendemail(gpsdata):
    COMMASPACE = ', '

    sender = 'lucafucciluca@gmail.com'
    gmail_password = ''
    recipients = ['luca.fucci@outlook.com']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Gpx Raspberry Output'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['Output.gpx']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email")
        raise



print("Connected")
try:
    while 1:
        gpsdata = []
        line = s.readline().decode('utf8')
        splittedLine = line.split(' ')
        print(splittedLine)
        if splittedLine[0]=="START":
            started = True
            firstStart = False
        while started:
            line = s.readline().decode('utf8')
            splittedLine = line.split(' ')
            print(splittedLine)
            if splittedLine[0]=='GPS:':
                gpsdata.append((splittedLine[1],splittedLine[2]))
            elif splittedLine[0]=="STOP":
                started = False
                print(gpsdata)
                printgpx(gpsdata)
                sendemail(gpsdata)

except KeyboardInterrupt:
    s.close()
