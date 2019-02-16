import paho.mqtt.client as mqtt
from time import strftime, sleep, time
import glob, os

light_stat = 0
run = True
mqtt_username = "pi"
mqtt_password = "raspberry"
mqtt_broker_ip = "192.168.4.1"
port = 1883
#clientID = "broker" 
mqtt_topic=[("node1/temp",0), ("node1/humid",0), ("node1/pressure",0), ("node2/soil", 0), ("node3/LEDStatus",0)]
node_timestamps = {}
node_stats = {}
node_codes = {
	'node1': 'BME280',
	'node2': 'KEYES2560_SH',
	'node3': 'KEYES2560_PIR'
}
path_to_db = '/home/pi/GUI/database/'
# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
	print ("Connected with Code :" +str(rc))
	client.subscribe(mqtt_topic)

	

# Callback Function on Receiving the Subscribed Topic/Message
def on_message(client, userdata, msg):
	# stamp the time message arrive wrt topic
	# global time
	node_name = msg.topic.split('/')[0]
	node_timestamps[node_name] = time()
	node_stats[node_name] = 1
	if (msg.topic == "node3/LEDStatus"):
		light_stat = int(msg.payload)
		print(msg.topic + ": " + str(light_stat) + "\n")
	else:
		data = float(msg.payload)
		t = round(float(strftime('%H')) + float(strftime('%M'))/60 + float(strftime('%S'))/3600, 2)
		mess = strftime('%Y,%m,%d') + ',' + str(t) + ',' + str(data) + '\n'
		print(mess)
		filename = path_to_db + msg.topic.split('/')[1] + '.csv'
		print(filename)
		with open(filename, 'a+') as file: 
			if file.tell() == 0:
				file.write('Year,Month,Day,Time,Value\n')
			file.write(mess) 
		file.close()

def clean_csv_files(files='/home/pi/GUI/database/*.csv'):
	for item in glob.glob(files):
		print('remove file ' + item)
		os.remove(item)

def main():
	# clean_csv_files()
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.username_pw_set(mqtt_username,mqtt_password)
	client.connect(host=mqtt_broker_ip, port=port, keepalive=60)

	# client.loop_forever()
	client.loop_start()
	while run:
		for node, val in node_timestamps.items():
			if time() - node_timestamps[node] >= 5:
				node_stats[node] = 0;
		filename = path_to_db + "device_list.csv"
		with open(filename, 'w') as file:
			for node, stat in node_stats.items():
				print("node " + node + ": " + str(stat))
				mess = node + ',' + node_codes[node] + ',unknown,' + str(stat) + '\n'
				file.write(mess)
			file.close()

		sleep(5)

	client.loop_stop(force=False)

if __name__ == "__main__":
	main()
