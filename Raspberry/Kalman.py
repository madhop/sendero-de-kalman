import serial
import time
s = serial.Serial('/dev/ttyACM0', 9600)
started = False

def printgpx(gpsdata):
    date= time.strftime("%c")
    gpxcontent = '<?xml version="1.0" encoding="UTF-8"?>\n\
<gpx version="1.0">\n\
    <name>Example gpx</name>\n\
        <trk>\n\
            <name>Example gpx</name><number>1</number>\n\
                <trkseg>\n'
    for point in gpsdata:
        gpxcontent += '\
                    <trkpt lat="'+point[0]+'" lon="'+point[1]+'"><ele>0</ele><time>'+point[2]+' '+point[3]+'</time></trkpt>\n'
    gpxcontent += '\
                </trkseg>\n\
        </trk>\n\
</gpx>'
    text_file = open(date+".gpx", "w")
    text_file.write(gpxcontent)
    text_file.close()

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
            s.write("START_OK \n".encode())
        while started:
            line = s.readline().decode('utf8')
            splittedLine = line.split(' ')
            print(splittedLine)
            if splittedLine[0]=='GPS:':
                gpsdata.append((splittedLine[1],splittedLine[2],splittedLine[3],splittedLine[4]))
            elif splittedLine[0]=="STOP":
                started = False
                print(gpsdata)
                #s.write("WRITING \n".encode())
                printgpx(gpsdata)
                s.write("STOP_OK \n".encode())
except KeyboardInterrupt:
    s.close()
