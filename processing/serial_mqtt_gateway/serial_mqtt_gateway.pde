/*
Install mqtt:
 Sketch::Import Library::Add Library, processing-mqtt, install
 */

import mqtt.*;
MQTTClient mqtt; // single server

void setup() {
  print("Started\n");
  size(1000, 500);
  background(255);
  textSize(24);
  fill(0);
  text("Started", 100, 100);
  
  setup_mqtt();
}

void draw() {
  delay(500);
}

void setup_mqtt() {
  mqtt = new MQTTClient(this); // must be this for callbacks or listener class
  print("Will connect...\n");
  mqtt.connect("mqtt://localhost:1883"); // no client-id on purpose
  mqtt.publish("awgrover/hello", "test");
}

void clientConnected() {
  print( "MQTT Connected\n" );
}

void connectionLost() {
  print( "MQTT Lost\n" );
}

void messageReceived(String topic, byte[] payload) {
}
