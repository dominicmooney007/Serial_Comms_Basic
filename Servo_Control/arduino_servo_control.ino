/*
  Servo Control Extension - Arduino Sketch
  Control a servo motor from Raspberry Pi via Serial Commands

  This sketch receives angle commands (0-180) from Raspberry Pi
  and controls a servo motor connected to the Arduino.

  Hardware Required:
  - Arduino Uno R3
  - Servo motor (e.g., SG90, MG90S, or similar)
  - USB cable connected to Raspberry Pi

  Wiring:
  - Servo Signal (Orange/Yellow) → Arduino Pin 9
  - Servo VCC (Red)             → Arduino 5V
  - Servo GND (Brown/Black)     → Arduino GND

  Instructions:
  1. Wire the servo motor as shown above
  2. Upload this sketch to your Arduino
  3. Run the Python servo control script on Raspberry Pi
  4. Enter angles (0-180) to control servo position

  Command Protocol:
  - Send angle as text: "90\n" (0-180 degrees)
  - Arduino responds: "Servo moved to: 90"
  - Invalid angles return error message

  Created: October 2025
  For: Servo Control Extension Project
*/

#include <Servo.h>

// Create servo object
Servo myServo;

// Configuration
const int SERVO_PIN = 9;        // PWM-capable pin
const int MIN_ANGLE = 0;        // Minimum servo angle
const int MAX_ANGLE = 180;      // Maximum servo angle
const int DEFAULT_ANGLE = 90;   // Starting position (center)

void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);

  // Wait for serial connection to establish
  delay(2000);

  // Attach servo to pin and set initial position
  myServo.attach(SERVO_PIN);
  myServo.write(DEFAULT_ANGLE);

  // Send startup message
  Serial.println("Arduino Servo Control Ready!");
  Serial.print("Servo initialized at ");
  Serial.print(DEFAULT_ANGLE);
  Serial.println(" degrees");
  Serial.println("Send angles 0-180 to control servo position");
}

void loop() {
  // Check if data has arrived
  if (Serial.available() > 0) {

    // Read the incoming message until newline character
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any whitespace

    // Convert string to integer
    int angle = command.toInt();

    // Validate angle range
    if (angle >= MIN_ANGLE && angle <= MAX_ANGLE) {
      // Valid angle - move servo
      myServo.write(angle);

      // Send confirmation
      Serial.print("Servo moved to: ");
      Serial.print(angle);
      Serial.println(" degrees");

    } else if (command.length() > 0 && command.toInt() == 0 && command != "0") {
      // Invalid input (not a number)
      Serial.print("Error: Invalid input '");
      Serial.print(command);
      Serial.println("' - Please send a number 0-180");

    } else {
      // Out of range
      Serial.print("Error: Angle ");
      Serial.print(angle);
      Serial.print(" out of range. Valid range: ");
      Serial.print(MIN_ANGLE);
      Serial.print("-");
      Serial.println(MAX_ANGLE);
    }
  }
}
