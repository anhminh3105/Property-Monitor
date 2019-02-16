#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

#define LDR A0
#define PIR D7
#define LED D5

int pirState;
int ldrValue;
int flag_mode=0;

volatile byte relayState = LOW;

// Timer Variables
long lastDebounceTime = 0;  
long debounceDelay = 10000;

const char* ssid = "WiPi";
const char* password = "raspberry";
const char* mqtt_server = "192.168.4.1";
const char* mqtt_username="pi";
const char* mqtt_password="raspberry";

char* LED_status="";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  //pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
  pinMode(PIR, INPUT);
  setupwifi();
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}
void loop(){
  if (!client.connected()) {
    reconnect();
  }
  client.publish("NodeStatus","CONNECTED!!");
  client.subscribe("LED");
  if(flag_mode==0){
    automatic();
  }
  client.publish("node3/LEDStatus",LED_status);
  client.loop();
  delay(250);
}
void setupwifi(){
  delay(10);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  if((char)payload[0] == '1'){ //Manual mode
    Serial.print("Manual mode ON!");
    flag_mode=1;
    if ((char)payload[1] == '1') {
      digitalWrite(LED, HIGH); 
      LED_status="1";  
      Serial.println(LED_status);
    } else {
      digitalWrite(LED, LOW); 
      LED_status="0"; 
      Serial.println(LED_status); 
    }
  }
  else{ //Automatic mode
    Serial.print("Automatic mode ON!");
    flag_mode=0;
  }
}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    WiFi.mode(WIFI_STA);
    if (client.connect("ESP8266_light",mqtt_username,mqtt_password)) {
      Serial.println("connected");
      
      //client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void automatic(){
  ldrValue = analogRead(LDR);
  Serial.print("Analog reading = ");
  Serial.println(ldrValue);
  if(relayState==HIGH) {
    LED_status="1";
    Serial.println(LED_status);
  }
  if(relayState==LOW) {
    LED_status="0";
    Serial.println(LED_status);
  }
  pirState = digitalRead(PIR);

  if (ldrValue <= 300 && pirState == HIGH) {
    digitalWrite(LED, HIGH);
    Serial.print("Analog reading = ");
    Serial.println(ldrValue);
    relayState = HIGH;
    LED_status="1";
    lastDebounceTime = millis();   
  }
  else if((ldrValue >= 600 && relayState == HIGH) || ((millis() - lastDebounceTime) >= debounceDelay && pirState == LOW)) {
    digitalWrite(LED, LOW);
    relayState = LOW;
    LED_status="0";
    Serial.print("Analog reading = ");
    Serial.println(ldrValue);
  }
}
