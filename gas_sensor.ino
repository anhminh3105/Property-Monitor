#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

int mqxx_analogPin = A0;
int buzzer=D8;
int sensorthresh=700;

const char* ssid     = "MinhTuan";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "Minhdo0309";     // The password of the Wi-Fi network
const char* mqttServer = "192.168.1.200";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "username";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "Minhdo0309";

WiFiClient espClient;
PubSubClient client(espClient);

void setup(){
  Serial.begin(115200);
  setupwifi();
  setupMQTT();
  pinMode(buzzer, OUTPUT);
}
void loop(){
  GasDetect();
  
  //delay(1000);
}
void setupwifi(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
}
void GasDetect(){
  
  int mqxx_value = analogRead(mqxx_analogPin);
  Serial.print(mqxx_value);
  Serial.print("  ");
  if(mqxx_value>sensorthresh){
    tone(buzzer, 1000); 
    delay(1000);       
    noTone(buzzer);     
    delay(1000);  
    client.publish("esp8266/FireAlarm", "WARNING,FIRE!!!!");
    delay(1000);
  }
  else{
    noTone(buzzer);
    client.publish("esp8266/FireAlarm", "NORMAL!!!");
    delay(1000);
  }
 
}
void setupMQTT(){
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("connected");

    } 
    else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
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
