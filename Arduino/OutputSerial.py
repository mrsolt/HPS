##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial
import time
import datetime
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

serial_port0 = '/dev/ttyACM7';
serial_port1 = '/dev/ttyACM8';
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
write_to_file0_path = "output.txt";
#write_to_file1_path = "output1.txt";

output_file0 = open(write_to_file0_path, "w+");
#output_file1 = open(write_to_file1_path, "w+");
ser0 = serial.Serial(serial_port0, baud_rate)
ser1 = serial.Serial(serial_port1, baud_rate)
i = 0
t = []
hum0 = []
temp0 = []
hum1 = []
temp1 = []
while True:
    line0 = ser0.readline();
    line0 = line0.decode("utf-8") #ser.readline returns a binary, convert to string
    line1 = ser1.readline();
    line1 = line1.decode("utf-8") #ser.readline returns a binary, convert to string
    if(i%100 == 0 and i != 0):
	writeout = str(time.time()) + " " + str(float(line0)) + " " + str(float(line1));
        print(writeout);
        output_file0.write(writeout);
        t.append(time.time());
        hum0.append(line0);
        hum1.append(line1);
        if(i%10000 == 0 and i != 0):
	    st = datetime.datetime.fromtimestamp(t[len(t)-1]).strftime('%Y-%m-%d %H:%M:%S')
	    save_st = datetime.datetime.fromtimestamp(t[len(t)-1]).strftime('%Y-%m-%d_%H-%M-%S')
	    fig, (ax0,ax1) = plt.subplots(nrows=1, ncols=2, figsize=(16,8));
            ax0.plot(t,hum0,label="Box A");
	    ax0.plot(t,hum1,label="Box B");
	    ax0.set_title('Humidity ' + st, fontsize=20);
	    ax0.legend(loc=1);
	    ax0.set_xlim(t[0],t[len(t)-1]);
	    ax0.set_xlabel('Time',fontsize=20)
	    ax0.set_ylabel('Relative Humididy %',fontsize=20)
	    #ax1.plot(t,temp0,label="Box A");
	    #ax1.plot(t,temp1,label="Box B");
	    #ax1.set_title('Temperature ' + st, fontsize=20);
	    #ax1.legend(loc=1);
	    #ax1.set_xlim(t[0],t[len(t)-1]);
	    #ax1.set_xlabel('Time',fontsize=20)
	    #ax1.set_ylabel('Temperature (C)',fontsize=20)
	    outfile = 'output_'+save_st
	    pp = PdfPages(outfile+'.pdf')
	    pp.savefig();
	    pp.close();
	    fig.savefig(outfile+'.png');
	    output_file0.close()
	    shutil.copyfile(write_to_file0_path, 'output_'+save_st+'.txt') 
	    output_file0 = open(write_to_file0_path, "w+");
	    print "Saved Fig!"
	    del t;
	    del hum0;
	    del temp0;
	    del hum1;
	    del temp1;
    	    t = [];
    	    hum0 = [];
    	    temp0 = [];
    	    hum1 = [];
    	    temp1 = [];
    i = i + 1;
