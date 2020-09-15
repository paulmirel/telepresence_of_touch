/* //<>// //<>//
 Install mqtt:
 Sketch::Import Library::Add Library, processing-mqtt, install
 */

import mqtt.*;
MQTTClient mqtt; // single server
Boolean mqtt_connected = false;
String mqtt_payload;
JSONObject mqtt_json_payload;
String mqtt_topic;
ArrayList<String> mqtt_topic_list = new ArrayList<String>();;

Serial arduino;
String arduino_input;

void setup() {
  print("Started\n");
  size(1000, 500);
  background(255);
  textSize(24);
  fill(0);
  text("Started", 100, 100);

  setup_arduino_serial(); // fixme: retry if serial lost
  // FIXME: wrap EVERYTHING with catch, close serial
  // maybe override PApplet.handleDraw & wrap
  setup_mqtt();
}

void draw() {
  if ( arduino_input != null ) {
    process_arduino_input();
  }
  process_arduino_output();
}

void debug_str_to_hex(String x) {
  int ct = 0;
  for ( int i : x.toCharArray()) {
    print( hex(i), "" );
    if (ct > 0 && ( (ct+1) % 8 == 0) ) {
      print( x.substring(ct-7, ct) );
      println();
    }
    ct += 1;
  }
  if ( !((ct+1) % 8 == 0) ) {
    print( x.substring(ct-7, ct) );
    println();
  }
}
// ----
void setup_arduino_serial() {
  arduino = connectUSBSerial(57600);
  arduino.bufferUntil(13);
}

void serialEvent(Serial p) {
  // assumes only the one serial-port

  // will get trailing \r
  // so remove it
  arduino_input = arduino.readString();
  arduino_input = arduino_input.substring(0, arduino_input.length()-1 );

  print("Serial: ");
  print(arduino_input);
  print("\n");
}

void process_arduino_input() {

  if ( arduino_input.startsWith("mqtt: ") ) {
    if (arduino_input.startsWith("mqtt: connect ")) {
      // mqtt: connect mqtt://x@x:some.host.wat:1883
      String url = arduino_input.replace("mqtt: connect ", "");
      //url = "mqtt://localhost:1883";
      print("Will connect '" + url + "'\n");
      //debug_str_to_hex(url);
      // FIXME: this blocks. timeout and retry?
      mqtt.connect(url); // no client-id on purpose
      mqtt_connected = true;

      //
    } else if (arduino_input.startsWith("mqtt: publish ") ) {
      if (mqtt_connected) {
        // FIXME validate the json, or at least warn if it is not
        mqtt.publish("awgrover/arduino", arduino_input.replace("mqtt: publish ", "") );
      } else {
        print("MQTT: not connected!");
      }
    } else if (arduino_input.startsWith("mqtt: subscribe ") ) {
      if (mqtt_connected) {
        String topic = arduino_input.replace("mqtt: subscribe ", "");

        mqtt.subscribe(topic);

        mqtt_topic_list.add( topic ); // need to keep track for reconnect
      } else {
        print("MQTT: not connected!");
      }
    }
  } else {
    // debug, leave it
  }
  arduino_input = null;
}

// ----
void setup_mqtt() {
  mqtt = new MQTTClient(this); // must be this for callbacks or listener class
}

void clientConnected() {
  print( "MQTT Connected, listening\n" );
  // all subscribes should happen "in" clientConnected,
  // so when MQTTClient automatically re-connects,
  // they will still be active,
  // If you don't subscribe in clientConnected(),
  // you'll no longer be subscribed upon lost/re-connect
  for (String topic : mqtt_topic_list ) {
    mqtt.subscribe(topic);
  }
}

void connectionLost() {
  // is detected pretty quick, ~ 1-3 seconds.
  // MQTTClient will re-connect automatically
  print( "MQTT Lost\n" );
}

void messageReceived(String topic, byte[] b_payload) {
  mqtt_topic = topic;

  // We expect a String...
  mqtt_payload = new String(b_payload);
  mqtt_json_payload = null;
  // Which is a json dictionary...
  try {
    mqtt_json_payload = parseJSONObject(mqtt_payload); // null if not json
  }
  catch (RuntimeException e) {
    if ( ! e.getMessage().startsWith("A JSONObject text must begin with") ) {
      throw(e);
    }
  }

  print("MQTT Received: ");
  print(topic);
  if ( mqtt_json_payload != null ) {
    print(" (json) ");
    // .getString("key", null); // won't throw
  } else {
    // wasn't a json dicationary
    print(" (string) ");
  }
  print(" : ");
  print(mqtt_payload);
  print("\n");
}

void process_arduino_output() {

  if ( arduino != null && mqtt_topic != null) {
    JSONObject serial_message = new JSONObject();
    serial_message.setString("topic", mqtt_topic);

    if (mqtt_json_payload != null ) {
      // send:
      serial_message.setJSONObject("payload", mqtt_json_payload );
    } else if ( mqtt_payload != null ) {
      serial_message.setString("payload", mqtt_payload );
    }

    // so typical, processing ALWAYS does multi-line pretty-format
    String compact = serial_message.format(0);
    compact = compact.replaceAll("\n", ""); // Danger, may whack \n in real data
    arduino.write("mqtt: message ");
    arduino.write( compact );
    arduino.write("\r");

    mqtt_topic = null;
    mqtt_json_payload = null; // done with it
    mqtt_payload = null; // done with it
  }
}
