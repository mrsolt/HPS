##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial
import time
import datetime
import shutil
import sys
import matplotlib.pyplot as plt
import tweepy
import Tkinter

consumer_key = 'oFiC72RXbiEJSaCjpreRxDQqV'
consumer_secret = 'XumkwpxAaVcZLhlIGgqr5x2B6o9YodwaAxOI6fPLtlgrN3paMM'
access_token = '1111079435434770433-U14SSWqCWXCw4B18CevdWOy5dHW6RR'
access_token_secret = 'BdlmHYOc8hJaZ3oTWiniTNCiPiYEikrzs79WIDHoIRAdx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name)
if(user.name != 'Heavy Photon Search'):
    print "User is not Heavy Photon Search. Exiting."
    sys.exit()

def tweetHumid(box):
    try:
        api.update_status(status = 'It is getting quite humid in here. Please Check Box {0}.'.format(box))
        print "Tweeted humidity!"
    except:
	print "Failed to tweet humididty {0}".format(box)

def tweetHumidStable(box):
    try:
        api.update_status(status = 'Humidity is now stable in Box {0}. Thank you for checking!'.format(box))
        print "Tweeted humidity stable!"
    except:
	print "Failed to tweet humididty stable {0}".format(box)

def tweetTemp(box):
    try:
        api.update_status(status = 'It is getting quite hot in here. Please Check Box {0}.'.format(box))
        print "Tweeted temperature!"
    except:
	print "Failed to tweet temperature {0}".format(box)

def tweetTempStable(box):
    try:
        api.update_status(status = 'Temperature is now stable in Box {0}. Thank you for checking!'.format(box))
        print "Tweeted temperature stable!"
    except:
	print "Failed to tweet temperature stable {0}".format(box)

def tweetBroken(box):
    try:
        api.update_status(status = 'I have lost connection to the test box. Please Check Box {0}.'.format(box))
        print "Tweeted lost connection!"
    except:
	print "Failed to tweet lost connection {0}".format(box)

def tweetPlot(image_path,st):
    tweet = 'Humidity and temperature results from {0}'.format(st)
    try:
        api.update_with_media(image_path, tweet)
        print "Tweeted updated image!"
    except:
	print "Failed to tweet updated image {0} at {1}".format(image_path,st)





serial_port0 = '/dev/ttyACM7';
serial_port1 = '/dev/ttyACM10';
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
write_to_file0_path = "output.txt";
data_rate = 1; #number of data points per second
plot_rate = 0.25; #number of plots per hour
data_int = int(baud_rate/float(data_rate)*0.1)
plot_int = int(baud_rate/float(plot_rate)*360.)

if(plot_int == 0):
    print "Check your plot rate!"
    sys.exit()

maxHum = 10
maxTemp = 99999
stableHum = 5
stableTemp = 99999
tweetHumA = False
tweetTempA = False
tweetHumB = False
tweetTempB = False
isAConnect = True
isBConnect = True

output_file0 = open(write_to_file0_path, "w+");
ser0 = serial.Serial(serial_port0, baud_rate)
ser1 = serial.Serial(serial_port1, baud_rate)
i = 0
t = []
hum0 = []
temp0 = []
hum1 = []
temp1 = []
while True:
    try:
        line0 = ser0.readline();
        line0 = line0.decode("utf-8") #ser.readline returns a binary, convert to string
    except:
	if(isAConnect):
	    tweetBroken('A')
	    isAConnect = False
	    print "Connection A broken"
	line0 = "1000"

    try:
	line1 = ser1.readline();
        line1 = line1.decode("utf-8") #ser.readline returns a binary, convert to string
    except:
	if(isBConnect):
	    tweetBroken('B')
	    isBConnect = False
	    print "Connection B broken"
	line1 = "1000"
    if(not isAConnect and not isBConnect):
        print "Lost connection to both Box A and Box B"
        sys.exit()
    #line0 = ser0.readline();
    #line0 = line0.decode("utf-8") #ser.readline returns a binary, convert to string
    #line1 = ser1.readline();
    #line1 = line1.decode("utf-8") #ser.readline returns a binary, convert to string
    if(i%data_int == 0 and i != 0):
	writeout = str(time.time()) + " " + str(float(line0)) + " " + str(float(line1));
        print("Time " + str(time.time()) + "  Humidity Box A " + str(float(line0)) + '%  Humidity Box B ' + str(float(line1)) + '%');
        output_file0.write(writeout);
        t.append(time.time());
        hum0.append(line0);
        hum1.append(line1);
	if(float(line0) > maxHum and not tweetHumA and isAConnect):
	    tweetHumid('A')
	    tweetHumA = True
	if(float(line1) > maxHum and not tweetHumB and isBConnect):
	    tweetHumid('B')
	    tweetHumB = True
	#if(line0 > maxTemp and not tweetTempA):
	#    tweetTemp('A')
	#    tweetTempA = True
	#if(line1 > maxTemp and not tweetTempB):
	#    tweetTemp('B')
	#    tweetTempB = True
	if(float(line0) < stableHum and tweetHumA):
	    tweetHumidStable('A')
	    tweetHumA = False
	    isHumAStable = True
	if(float(line1) < stableHum and tweetHumB):
	    tweetHumB = False
	    tweetHumidStable('B')
	    isHumBStable = True
	#if(line0 < stableTemp  and tweetTempA):
	#    tweetTempStable('A')
	#    tweetTempA = False
	#if(line1 < stableTemp and tweetTempB):
	#    tweetTempStable('B')
	#    tweetTempB = False
        if(i%plot_int == 0 and i != 0):
	    st = datetime.datetime.fromtimestamp(t[len(t)-1]).strftime('%Y-%m-%d %H:%M:%S')
	    save_st = datetime.datetime.fromtimestamp(t[len(t)-1]).strftime('%Y-%m-%d_%H-%M-%S')
	    #fig, (ax0,ax1) = plt.subplots(nrows=1, ncols=2, figsize=(16,8));
	    fig, (ax0) = plt.subplots(nrows=1, ncols=1, figsize=(8,8));
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
	    outfile = 'output_'+save_st+'.png'
	    fig.savefig(outfile);
	    output_file0.close()
	    shutil.copyfile(write_to_file0_path, 'output_'+save_st+'.txt') 
	    output_file0 = open(write_to_file0_path, "w+");
	    tweetPlot(outfile,st)
	    print "Saved Fig! Tweeted Fig!"
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
	    i = 0;
    i = i + 1;
