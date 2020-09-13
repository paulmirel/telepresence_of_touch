/* //<>// //<>//
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
  mqtt.subscribe("awgrover/#");
}

void clientConnected() {
  print( "MQTT Connected\n" );
}

void connectionLost() {
  print( "MQTT Lost\n" );
}

void messageReceived(String topic, byte[] b_payload) {
  // We expect a String...
  String payload = new String(b_payload);
  JSONObject json_payload = null;
  // Which is a json dictionary...
  try {
    json_payload = parseJSONObject(payload); // null if not json
  }
  catch (RuntimeException e) {
    if ( ! e.getMessage().startsWith("A JSONObject text must begin with") ) {
      throw(e);
    }
  }

  print("Received: ");
  print(topic);
  if ( json_payload != null ) {
    print(" (json) ");
  } else {
    // wasn't a json dicationary
    print(" (string) ");
  }
  print(" : ");
  print(payload);
  print("\n");
}
