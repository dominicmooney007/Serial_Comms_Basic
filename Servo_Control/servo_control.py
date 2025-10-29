#!/usr/bin/env python3
"""
Servo Control Extension - Python Script
Interactive Servo Motor Control from Raspberry Pi

This script provides an interactive interface to control a servo motor
connected to an Arduino via serial communication.

Hardware Required:
- Raspberry Pi 5
- Arduino Uno R3 with servo motor attached
- USB A to B cable

Servo Wiring on Arduino:
- Servo Signal (Orange/Yellow) → Pin 9
- Servo VCC (Red)             → 5V
- Servo GND (Brown/Black)     → GND

Before running:
1. Wire the servo to Arduino Pin 9
2. Upload arduino_servo_control.ino to your Arduino
3. Close the Arduino Serial Monitor
4. Verify the port is /dev/ttyACM0 (or change in code below)

Usage:
    python3 servo_control.py              # Interactive mode
    python3 servo_control.py 90           # Move to 90 degrees and exit
    python3 servo_control.py --help       # Show help

Interactive Commands:
- Enter angle (0-180): Move servo to specified position
- 'q' or 'quit': Exit program
- 'h' or 'help': Show help
- 'c' or 'center': Move servo to center (90 degrees)

Created: October 2025
For: Servo Control Extension Project
"""

import serial
import time
import sys

# Configuration
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
MIN_ANGLE = 0
MAX_ANGLE = 180
CENTER_ANGLE = 90

def print_help():
    """Display help information"""
    print("\n=== Servo Control Help ===")
    print("Commands:")
    print("  0-180        : Move servo to specified angle")
    print("  c, center    : Move servo to center position (90°)")
    print("  h, help      : Show this help message")
    print("  q, quit      : Exit program")
    print("\nExamples:")
    print("  90           : Move to 90 degrees (center)")
    print("  0            : Move to 0 degrees (far left)")
    print("  180          : Move to 180 degrees (far right)")
    print("========================\n")

def send_angle(ser, angle):
    """
    Send angle command to Arduino and read response

    Args:
        ser: Serial connection object
        angle: Servo angle (0-180)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Send angle command
        command = f"{angle}\n"
        ser.write(command.encode())

        # Wait for response
        time.sleep(0.1)

        # Read response
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"  → {response}")
            return True
        else:
            print(f"  → Warning: No response from Arduino")
            return False

    except Exception as e:
        print(f"  → Error sending command: {e}")
        return False

def validate_angle(angle_str):
    """
    Validate angle input

    Args:
        angle_str: String input from user

    Returns:
        int or None: Valid angle or None if invalid
    """
    try:
        angle = int(angle_str)
        if MIN_ANGLE <= angle <= MAX_ANGLE:
            return angle
        else:
            print(f"  → Error: Angle must be between {MIN_ANGLE} and {MAX_ANGLE}")
            return None
    except ValueError:
        print(f"  → Error: '{angle_str}' is not a valid number")
        return None

def interactive_mode(ser):
    """
    Run interactive servo control mode

    Args:
        ser: Serial connection object
    """
    print("\n=== Interactive Servo Control ===")
    print("Enter angles (0-180) to control the servo")
    print("Type 'h' for help, 'q' to quit\n")

    # Read and display Arduino startup messages
    time.sleep(0.5)
    while ser.in_waiting > 0:
        startup_msg = ser.readline().decode().strip()
        if startup_msg:
            print(f"Arduino: {startup_msg}")

    print("\nReady for commands!")

    while True:
        try:
            # Get user input
            user_input = input("\nEnter command: ").strip().lower()

            # Handle special commands
            if user_input in ['q', 'quit', 'exit']:
                print("Exiting servo control...")
                break

            elif user_input in ['h', 'help', '?']:
                print_help()
                continue

            elif user_input in ['c', 'center']:
                print(f"Moving to center position ({CENTER_ANGLE}°)...")
                send_angle(ser, CENTER_ANGLE)
                continue

            elif user_input == '':
                continue

            # Try to parse as angle
            angle = validate_angle(user_input)
            if angle is not None:
                print(f"Moving servo to {angle}°...")
                send_angle(ser, angle)

        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break

def single_command_mode(ser, angle):
    """
    Send a single angle command and exit

    Args:
        ser: Serial connection object
        angle: Servo angle to set
    """
    # Read Arduino startup messages
    time.sleep(0.5)
    while ser.in_waiting > 0:
        ser.readline()  # Clear buffer

    print(f"Setting servo to {angle}°...")
    success = send_angle(ser, angle)

    if success:
        print("Command sent successfully!")
    else:
        print("Failed to send command")
        sys.exit(1)

def main():
    """Main program entry point"""

    # Check for command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h', 'help']:
            print(__doc__)
            sys.exit(0)

        # Single command mode
        angle = validate_angle(sys.argv[1])
        if angle is None:
            print(f"Error: Invalid angle '{sys.argv[1]}'")
            print("Usage: python3 servo_control.py [angle]")
            print("       angle must be between 0 and 180")
            sys.exit(1)

        mode = 'single'
        target_angle = angle
    else:
        mode = 'interactive'

    try:
        # Connect to Arduino
        print(f"Connecting to Arduino on {SERIAL_PORT}...")
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset - CRITICAL!
        print("Connected!\n")

        # Run appropriate mode
        if mode == 'single':
            single_command_mode(ser, target_angle)
        else:
            interactive_mode(ser)

        # Close connection
        ser.close()
        print("\nConnection closed. Goodbye!")

    except serial.SerialException as e:
        print(f"\n✗ Error: Could not open serial port {SERIAL_PORT}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Is the Arduino connected?")
        print("2. Is the Arduino Serial Monitor closed?")
        print("3. Do you have permission? Try:")
        print(f"   sudo chmod 666 {SERIAL_PORT}")
        print("4. Check available ports:")
        print("   ls /dev/ttyACM*")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
        try:
            ser.close()
        except:
            pass

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
