/* //<>// //<>//
Install mqtt:
 Sketch::Import Library::Add Library, processing-mqtt, install
 */

import mqtt.*;
MQTTClient mqtt; // single server
Serial arduino;

void setup() {
  print("Started\n");
  size(1000, 500);
  background(255);
  textSize(24);
  fill(0);
  text("Started", 100, 100);

  setup_arduino_serial();
  setup_mqtt();
}

void draw() {
}

// ----
void setup_arduino_serial() {
  arduino = connectUSBSerial(57600);
  arduino.bufferUntil(13);
}

void serialEvent(Serial p) {
  // assumes only the one serial-port
  String arduino_input = arduino.readString();
  print("Serial: ");
  print(arduino_input);
  print("\n");
  mqtt.publish("awgrover/arduino", arduino_input );
}

// ----
void setup_mqtt() {
  mqtt = new MQTTClient(this); // must be this for callbacks or listener class
  print("Will connect...\n");
  // FIXME: this blocks. timeout and retry?
  mqtt.connect("mqtt://localhost:1883"); // no client-id on purpose
  mqtt.publish("awgrover/hello", "test");
}

void clientConnected() {
  print( "MQTT Connected, listening\n" );
  // all subscribes should happen "in" clientConnected,
  // so when MQTTClient automatically re-connects,
  // they will still be active,
  // If you don't subscribe in clientConnected(),
  // you'll no longer be subscribed upon lost/re-connect
  mqtt.subscribe("awgrover/#");
}

void connectionLost() {
  // is detected pretty quick, ~ 1-3 seconds.
  // MQTTClient will re-connect automatically
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
    // .getString("key", null); // won't throw
  } else {
    // wasn't a json dicationary
    print(" (string) ");
  }
  print(" : ");
  print(payload);
  print("\n");
}
