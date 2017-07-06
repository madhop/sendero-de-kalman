import serial
array = [('45.820201','9.253241'),('45.819408','9.252908'),('45.818556','9.252436')]

s = serial.Serial('/dev/ttyACM0', 9600)
gpsdata = []
print("Connected")
gpscount = 0
while gpscount<5:
    line = s.readline().decode('utf8')
    splittedLine = line.split(' ')
    print(splittedLine)
    if splittedLine[0]=='GPS:':
        gpsdata.append((splittedLine[1],splittedLine[2]))
        gpscount+=1
print(gpsdata)
s.close()

gpxcontent = '\
<?xml version="1.0" encoding="UTF-8"?>\n\
<gpx version="1.0">\n\
	<name>Example gpx</name>\n\
	<trk><name>Example gpx</name><number>1</number><trkseg>\n'
for point in gpsdata:
    gpxcontent+='            <trkpt lat="'+point[0]+'" lon="'+point[1]+'"><ele>0</ele><time>2007-10-14T10:09:57Z</time></trkpt>\n'
gpxcontent += '\
	</trkseg></trk>\n\
</gpx>\
'

text_file = open("Output.gpx", "w")
text_file.write(gpxcontent)
text_file.close()
