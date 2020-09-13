import processing.serial.*;

Serial connectUSBSerial(int baud) {
  // return a Serial object that we think is the usb-serial (arduino), or null
  String[] flipDotPorts = Serial.list();
  println(flipDotPorts);

  String arduinoPortName = null;
  for (int i = 0; i < flipDotPorts.length; i++) {
    if (
      // guess, based on historical names of ports
      // We are taking the first 1
      flipDotPorts[i].contains("ACM") // linux more fully: /dev/ttyACM0
      || flipDotPorts[i].contains("cu.usbmodem") // mac
      || flipDotPorts[i].contains("tty. usbmodem") // linux
      ) { 
      arduinoPortName = flipDotPorts[i];
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
