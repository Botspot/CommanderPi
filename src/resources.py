import os
import subprocess as sp
import fileinput
import configparser
import psutil
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
home_path = sys.argv[1]

config = configparser.ConfigParser()
if os.path.exists(home_path+'/CommanderPi/src/cpi.config'):
	config.read(home_path+'/CommanderPi/src/cpi.config')
	print("Exist and read")
else:
	print("Creating config...")
	config['DEFAULT'] = {'color_mode': '0',
	'version': '0.4.2'}
	with open(home_path+'/CommanderPi/src/cpi.config', 'w') as configfile:
		config.write(configfile)

### update stuff
app_version = "Version 0.4.2\n"
def getAppVersion():
	return app_version

### Open url link
def cpi_open_url(link):
	os.system('sudo -upi chromium-browser '+link)

### NETWORK stuff
eth0 = sp.getoutput('sudo ifconfig eth0')
ipv4eth = "Not set up"
ipv6eth = "Not set up"
mac = ""
for line in eth0.splitlines():
		if "netmask" in line:
			ipv4eth = line[13:26]
		if "inet6" in line:
			ipv6eth = line[14:38]
		if "ether" in line:
			mac = line[14:32]
eth0_data = "IPv4 "+ipv4eth+"\nIPv6 "+ipv6eth+"\nMAC "+mac

wlan0 = sp.getoutput('sudo ifconfig wlan0')
ipv4wlan0 = "Not set up"
ipv6wlan0 = "Not set up"
macwlan0 = ""
for line in wlan0.splitlines():
		if "netmask" in line:
			ipv4wlan0 = line[13:26]
		if "inet6" in line:
			ipv6wlan0 = line[14:38]
		if "ether" in line:
			macwlan0 = line[14:32]
wlan0_data = "IPv4 "+ipv4wlan0+"\nIPv6 "+ipv6wlan0+"\nMAC "+macwlan0


### DEPRACTED
ethernet_driver = sp.getoutput('sudo ethtool -i eth0')
wlan_driver = sp.getoutput('sudo ethtool -i wlan0')


### DISK SPACE 
hdd = psutil.disk_usage('/')
def get_total_space():
	return hdd.total / (2**30)
def get_used_space():
	return hdd.used / (2**30)
def get_free_space():
	return hdd.free / (2**30)
def get_disk_percent():
	return hdd.percent

total = str(round(get_total_space(), 2))
used = str(round(get_used_space(), 2))
free = str(round(get_free_space(),2))
disk = str(get_disk_percent())
print (hdd.percent)
print ("Total: " + total)
print ("Used: " + used)
print ("Free: " + free)


img_path = os.path.dirname('logo.png')



#### Check entry in gui is preesed
push_state1 = False
push_state2 = False
push_state3 = False
def set_push_state(state):
	global push_state1
	global push_state2
	global push_state3
	if ( state == 1 ):
		push_state1 = True
	elif ( state == 2):
		push_state2 = True
	elif (state == 3):
		push_state3 = True

def getproc0():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 1 | sed -e s/$/:/')
	cpux = str(cpu)
	return cpux
	
def getproc1():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 2 | sed -e s/^[[:space:]]*//')
	cpux = str(cpu)
	return cpux
### Reboot RPI	
def reboot():
	os.system("sudo reboot now")
	
cpu_usage_path = "build/cpu_usage.txt"
temperature = "build/actual_temp.txt"



#cpu_usagex = sp.getoutput('vcgencmd measure_clock arm')
def refusage():
	cpu_usagex = sp.getoutput('vcgencmd measure_clock arm')
	cpu_usage = ""
	buff=cpu_usagex[14:17]
	buff=int(buff)
	buffg=cpu_usagex[14:15]
	buffm=cpu_usagex[15:16]
	if ( buff < 500 ):
		cpu_usage = buffg+ "." + buffm + "GHz"
	else:
		buff = str(buff)
		cpu_usage = buff + "MHz"
	return cpu_usage
	
	
def refmem():
	memory_usex = psutil.virtual_memory().percent
	memory_use = str(memory_usex)
	return memory_use

temperature = sp.getoutput('vcgencmd measure_temp')
def reftemp():
	tempx = sp.getoutput('vcgencmd measure_temp')
	temp=tempx[5:]
	return temp
	
	
	
	
	### BOARD VERSION ###
board_versionx = sp.getoutput('cat /proc/device-tree/model')
board_version = board_versionx[:-1]

def get_board_version():
	if "Pi 3 Model B Plus" in board_version:
		return 3
	if "Pi 4 Model" in board_version:
		return 4
		
	


	
processor_architecture = sp.getoutput('uname -m')
host_name = sp.getoutput('uname -n')
system_name = sp.getoutput('uname')
kernel_version = sp.getoutput('uname -r')

config_path = "/boot/config.txt"
gpu_freq = "400" #default
gexist = False

arm_freq = "1500" #default
aexist = False

over_voltage = "4" #default
oexist = False
f = open(config_path)
for line in f:


	if "arm_freq" in line:
		arm_freq = line
		aexist = True
	if "gpu_freq" in line:
		gpu_freq = line
		gexist = True
	if "over_voltage" in line:
		over_voltage = line
		oexist = True
		
f.close()




def overclock_over_voltage(new_over_voltage):
	global oexist
	if oexist:
		
		fin = open(config_path, "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(over_voltage, 'over_voltage='+new_over_voltage+'\n')
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open(config_path, "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		print(new_over_voltage)
		new_over_voltage = None
	else:
		oexist = True
		file_object = open(config_path, 'a')
		file_object.write('over_voltage='+new_over_voltage+'\n')
		file_object.close()

def overclock_gpu_freq(gpu_new_freq):
	global gexist
	if gexist:
		
		fin = open(config_path, "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(gpu_freq, 'gpu_freq='+gpu_new_freq+'\n')
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open(config_path, "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		print(gpu_new_freq)
		gpu_new_freq = None
	else:
		gexist = True
		file_object = open(config_path, 'a')
		file_object.write('gpu_freq='+gpu_new_freq+'\n')
		file_object.close()
		
		

def overclock_arm_freq(arm_new_freq):
	global aexist
	if aexist:

		fin = open(config_path, "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(arm_freq, 'arm_freq='+arm_new_freq+'\n')
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open(config_path, "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		print(arm_new_freq)
		arm_new_freq = None
	else:
		aexist = True
		file_object = open(config_path, 'a')
		file_object.write('arm_freq='+arm_new_freq+'\n')
		file_object.close()		
