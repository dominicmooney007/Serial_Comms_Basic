#!/usr/bin/env python3
"""
Quick Start Guide - Two-Way Communication
Raspberry Pi and Arduino Bidirectional Communication

This script sends a message to Arduino and reads the response back.

Hardware Required:
- Raspberry Pi 5
- Arduino Uno R3
- USB A to B cable

Before running:
1. Upload arduino_twoway.ino to your Arduino
2. Close the Arduino Serial Monitor
3. Verify the port is /dev/ttyACM0 (or change in code below)

Usage:
    python3 test_twoway.py

Created: October 2025
For: Quick Start Guide - Two-Way Communication Example
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

try:
    # Connect to Arduino
    print("Connecting to Arduino...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset - CRITICAL!

    # Send message
    message = "Hello Arduino!"
    print(f"Sending: {message}")
    ser.write(message.encode() + b'\n')

    # Wait and read response
    print("Waiting for response...")
    time.sleep(1)

    if ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        print(f"Arduino replied: {response}")
    else:
        print("No response from Arduino (timeout)")

    ser.close()
    print("\nCommunication complete!")

except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}")
    print(f"Details: {e}")
    print("\nTroubleshooting:")
    print("1. Is the Arduino connected?")
    print("2. Is the Arduino Serial Monitor closed?")
    print("3. Try: sudo chmod 666 /dev/ttyACM0")
    print("4. Check port: ls /dev/ttyACM*")

except KeyboardInterrupt:
    print("\nProgram interrupted by user")

except Exception as e:
    print(f"Unexpected error: {e}")
