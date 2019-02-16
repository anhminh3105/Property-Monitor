/*
  # 0  ~300     dry soil -- 0~ 
  # 300~700     humid soil
  # 700~950     in water
*/
#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

const int ledPin = 13; // This code uses the built-in led for visual feedback that the button has been pressed
const int soil_analogue_input = 17;

// WiFi
// Make sure to update this for your own WiFi network!
const char* ssid = "WiPi";
const char* wifi_password = "raspberry";

// MQTT
// Make sure to update this for your own MQTT Broker!
const char* mqtt_server = "192.168.4.1";
const char* mqtt_topic = "node2/soil";
const char* mqtt_username = "pi";
const char* mqtt_password = "raspberry";
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "ESP8266_soil";

// Initialise the WiFi and MQTT Client objects`
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker


void setup() {
  pinMode(ledPin, OUTPUT);

  // Switch the on-board LED off to start with
  digitalWrite(ledPin, LOW);

  // Begin Serial on 9600 for debugging purposes
  Serial.begin(9600);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}
/*
char *get_soil_condition(int soil_analogue_value) {
  if (soil_analogue_value < 300) {
    return "dry soil";
  }
  else if (soil_analogue_value < 700) {
    return "humid soil: ";
  }
  else if (soil_analogue_value < 950) {
    return "in water";
  }
  return "value out of range";
}
*/

int get_soil_moisture_in_percent(int soil_analogue_value) {
  int max = 950;
  if (soil_analogue_value >= 0 && soil_analogue_value <= max) {
    return (soil_analogue_value * 100 / max);
  }
  return -1;
}

void loop() {
  // put your main code here, to run repeatedly.
  int val = analogRead(soil_analogue_input);
  int soil_moisture_percent = get_soil_moisture_in_percent(val);
  Serial.println(soil_moisture_percent);
     if (client.publish(mqtt_topic, String(soil_moisture_percent).c_str())) {
      Serial.println("message sent!");
      digitalWrite(ledPin, HIGH);
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      WiFi.mode(WIFI_STA);
      client.connect(clientID, mqtt_username, mqtt_password);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      client.publish(mqtt_topic, "Button pressed!");
    }
  digitalWrite(ledPin, LOW);
  delay(1000);
}
