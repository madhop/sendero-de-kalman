import serial
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

except KeyboardInterrupt:
    s.close()
