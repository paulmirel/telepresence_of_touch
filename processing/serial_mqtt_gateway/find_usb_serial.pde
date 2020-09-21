import processing.serial.*;

Serial connectUSBSerial(int baud) {
  // return a Serial object that we think is the usb-serial (arduino), or null
  String[] arduino_ports = Serial.list();
  println(arduino_ports);

  String arduinoPortName = null;
  for (int i = 0; i < arduino_ports.length; i++) {
    if (
      // guess, based on historical names of ports
      // We are taking the first 1
      arduino_ports[i].contains("ACM") // linux more fully: /dev/ttyACM0
      || arduino_ports[i].contains("cu.usbmodem") // mac
      || arduino_ports[i].contains("tty. usbmodem") // windows
      ) { 
      arduinoPortName = arduino_ports[i];
    }
  }

  if (arduinoPortName != null) {
    print("Connected to ");
    println(arduinoPortName);
    return new Serial( this, arduinoPortName, baud);
  } else {
    println("Failed to find an usb serial");
    return null;
  }
}
