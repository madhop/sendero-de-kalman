import serial
array = [('45.820201','9.253241'),('45.819408','9.252908'),('45.818556','9.252436')]
'''
s = serial.Serial('/dev/ttyACM0', 9600)
print("Connected")
while 1:
    #line = s.readline().decode('utf8')
    #splittedLine = line.split(' ')
    print(s.readline())

s.close()
'''
content = '\
<?xml version="1.0" encoding="UTF-8"?>\n\
<gpx version="1.0">\n\
	<name>Example gpx</name>\n\
	<trk><name>Example gpx</name><number>1</number><trkseg>\n'
for point in array:
    content+='            <trkpt lat="'+point[0]+'" lon="'+point[1]+'"><ele>0</ele><time>2007-10-14T10:09:57Z</time></trkpt>\n'
content += '\
	</trkseg></trk>\n\
</gpx>\
'

text_file = open("Output.gpx", "w")
text_file.write(content)
text_file.close()
