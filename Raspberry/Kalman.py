import serial
import time
import csv
import os
s = serial.Serial('/dev/ttyACM0', 9600)
started = False
def printgpx(gpsdata, date):

    gpxcontent = '<?xml version="1.0" encoding="UTF-8"?>\n\
<gpx version="1.0">\n\
    <name>Example gpx</name>\n\
        <trk>\n\
            <name>Example gpx</name><number>1</number>\n\
                <trkseg>\n'
    for point in gpsdata:
        gpxcontent += '\
                    <trkpt lat="'+point[0]+'" lon="'+point[1]+'"><ele>0</ele><time>'+point[2]+'</time></trkpt>\n'
    gpxcontent += '\
                </trkseg>\n\
        </trk>\n\
</gpx>'
    text_file = open(date+"/Output.gpx", "w")
    text_file.write(gpxcontent)
    text_file.close()

print("Connected")
try:
    while 1:
        gpsdata = []
        accdata = []
        line = s.readline().decode('utf8')
        splittedLine = line.split(' ')
        print(splittedLine)
        if splittedLine[0]=="START":
            started = True
            firstStart = False
            s.write("START_OK \n".encode())
        while started:
            line = s.readline().decode('utf8')
            splittedLine = line.split(' ')
            print(splittedLine)
            if splittedLine[0]=='GPS:':
                #gpsdata.append((splittedLine[1],splittedLine[2],splittedLine[3],splittedLine[4])) #per tempo dato dal gps
                gpsdata.append((splittedLine[1],splittedLine[2],splittedLine[3])) #per tempo dato da arduino
            elif splittedLine[0]=='ACC:':
                accdata.append((splittedLine[1],splittedLine[2],splittedLine[3],splittedLine[4]))
            elif splittedLine[0]=="STOP":
                started = False
                #print(gpsdata)
                #s.write("WRITING \n".encode())
                date= time.strftime("%c")
                newpath = (date)
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                printgpx(gpsdata, date)
                with open(date+'/gps.csv', 'w', newline="") as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',')
                    for row in gpsdata:
                        spamwriter.writerow([row[0],row[1],int(row[2])])
                with open(date+'/acc.csv', 'w', newline="") as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',')
                    for row in accdata:
                        spamwriter.writerow([row[0],row[1],row[2],int(row[3])])
                s.write("STOP_OK \n".encode())
except KeyboardInterrupt:
    s.close()
