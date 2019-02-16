#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;
#define SEALEVELPRESSURE_HPA (1013.25)

const char* ssid = "WiPi";                   // wifi ssid
const char* password =  "raspberry";         // wifi password
const char* mqttServer = "192.168.4.1";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "pi";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "raspberry";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(mqttServer, mqttPort, espClient);

void setup() {
  Serial.begin(9600);
  setupwifi();
  setupMQTT();
  setupBME280();
}



void loop() {
  /*float x=1.000343434;
  client.publish("esp8266", String(x).c_str());
  client.subscribe("esp8266");
  delay(300);
  client.loop();*/
  float temp = bme.readTemperature();
  float humid = bme.readHumidity();
  float pressure = bme.readPressure();
  //Serial.print(temp);
  
  if(client.publish("node1/temp", String(temp).c_str())) {
    Serial.print("send message temp = ");
    Serial.println(temp);
  }
  delay(150);
  if(client.publish("node1/humid", String(humid).c_str())) {
    Serial.print("send message humid = ");
    Serial.println(humid);
  }
  delay(150);  
  if(client.publish("node1/pressure", String(pressure).c_str())) {
    Serial.print("send message pressure = ");
    Serial.println(pressure);
  }
  //client.subscribe("esp8266");
  delay(500);
  // client.loop();
   
}
void setupwifi(){
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Connected with IP address: ");
  Serial.println(WiFi.localIP());
}

void setupMQTT(){
  // client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266_BME280", mqttUser, mqttPassword )) {
      Serial.println("connected");

    } 
    else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void setupBME280(){
  bool status;
  status = bme.begin();  
  if (!status) {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }
}
void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------");

}
