#include "ESP8266WiFi.h"
 
const char* ssid = "lemur";
const char* password =  "lemur9473";
 
WiFiServer wifiServer(80);
 
void setup() {

pinMode(LED_BUILTIN, OUTPUT); //GPIO16 is an OUTPUT pin;
digitalWrite(LED_BUILTIN, HIGH); //Initial state is OFF
 
  Serial.begin(115200);
 
  delay(1000);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
 
  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());
 
  wifiServer.begin();
}
 
void loop() {
 
  WiFiClient client = wifiServer.available();
 
  if (client) {
 
    while (client.connected()) {
 
      while (client.available()>0) {
        char c = client.read();
        Serial.write("Here is the client msg:\n");
        Serial.write(c);
        Serial.write("\n");
        if (c == '1')
        {
          digitalWrite(LED_BUILTIN, LOW);
        }
        else if (c == '0')
        {
          digitalWrite(LED_BUILTIN, HIGH);
        }
      }
 
      delay(10);
    }
 
    client.stop();
    Serial.println("\nClient disconnected");
 
  }
}
