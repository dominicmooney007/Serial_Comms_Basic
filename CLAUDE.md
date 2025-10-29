# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Serial_Comms_Basic is an educational project teaching bidirectional serial communication between a Raspberry Pi 5 and Arduino Uno R3. The project uses Python 3 with PySerial on the Raspberry Pi side and Arduino C/C++ on the microcontroller side, communicating over USB at 9600 baud.

## Technology Stack

- **Raspberry Pi**: Python 3 with PySerial library
- **Arduino**: Arduino Uno R3 with built-in Serial library
- **Communication**: UART over USB (appears as `/dev/ttyACM0`)
- **Protocol**: ASCII text with newline delimiters

## Essential Development Commands

### System Setup
```bash
# Install Arduino IDE
sudo apt update && sudo apt install arduino -y

# Install PySerial
pip3 install pyserial

# Configure permissions (required for serial port access)
sudo usermod -a -G dialout $USER
sudo usermod -a -G tty $USER
sudo reboot  # Required after group changes
```

### Connection Verification
```bash
# Check Arduino connection
lsusb | grep Arduino
ls /dev/ttyACM*

# Test PySerial installation
python3 -c "import serial; print('PySerial installed successfully!')"

# Verify user has correct permissions
groups $USER  # Should include dialout and tty
```

### Running Examples
```bash
# One-way communication (after uploading arduino_receiver.ino)
python3 test_serial.py

# Two-way communication (after uploading arduino_twoway.ino)
python3 test_twoway.py
```

### Troubleshooting
```bash
# Fix permissions temporarily (not persistent)
sudo chmod 666 /dev/ttyACM0

# Check syntax without hardware
python3 -m py_compile test_serial.py
```

## Architecture and Patterns

### Communication Architecture

The project implements a request-response pattern over serial UART:
- **Transport**: USB cable creates virtual serial port (`/dev/ttyACM0`)
- **Baud Rate**: 9600 bps (standardized across all examples)
- **Message Format**: ASCII text terminated with `\n` (newline)
- **Encoding**: UTF-8 in Python, String in Arduino

### Code Organization Pattern

The project uses **paired examples** where each communication pattern has matching Python and Arduino implementations:

1. **One-Way Pair**: `test_serial.py` → `arduino_receiver.ino`
2. **Two-Way Pair**: `test_twoway.py` ↔ `arduino_twoway.ino`

### Critical Timing Requirements

**⚠️ IMPORTANT**: Arduino boards auto-reset when a serial connection is established. Both Python and Arduino code implement a **mandatory 2-second delay** after connection:

```python
# Python side
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # CRITICAL: Wait for Arduino to reset
```

```cpp
// Arduino side
void setup() {
    Serial.begin(9600);
    delay(2000);  // CRITICAL: Stabilization time
}
```

Removing these delays will cause communication failures.

### Message Encoding Pattern

**Python sending:**
```python
ser.write("message".encode())  # String to bytes
ser.write(b'\n')               # Delimiter
```

**Python receiving:**
```python
response = ser.readline().decode().strip()  # Bytes to string, remove whitespace
```

**Arduino receiving:**
```cpp
if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');  // Wait for delimiter
}
```

**Arduino sending:**
```cpp
Serial.println(message);  // Automatically adds \n
```

### Exclusive Port Access Pattern

**⚠️ CRITICAL**: Only one program can access the serial port at a time:
- Arduino Serial Monitor and Python scripts are mutually exclusive
- Close Arduino Serial Monitor before running Python scripts
- Close Python scripts before opening Arduino Serial Monitor

Attempting simultaneous access will result in `SerialException: [Errno 16] Device or resource busy`.

## Standard Configuration

All code uses these standardized settings:

| Setting | Value |
|---------|-------|
| Serial Port | `/dev/ttyACM0` |
| Baud Rate | `9600` |
| Timeout | `1` second |
| Message Delimiter | `\n` (newline) |

When modifying or extending examples, maintain these constants for compatibility.

## Python Script Structure

All Python scripts follow this pattern:

```python
#!/usr/bin/env python3
"""Module docstring"""
import serial
import time

# Configuration constants
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

try:
    # Main logic with 2-second delay after connection
except serial.SerialException:
    # Handle port access errors
except KeyboardInterrupt:
    # Handle user cancellation
except Exception as e:
    # Handle unexpected errors
finally:
    ser.close()  # Always cleanup
```

## Arduino Sketch Structure

All Arduino sketches follow this pattern:

```cpp
// File header with purpose

void setup() {
    Serial.begin(9600);
    delay(2000);  // CRITICAL: Stabilization
    // Optional: startup messages
}

void loop() {
    if (Serial.available() > 0) {
        String message = Serial.readStringUntil('\n');
        // Process message
        // Optional: send response with Serial.println()
    }
}
```

## Common Error Patterns

**Permission Denied (`/dev/ttyACM0`):**
- User not in `dialout` and `tty` groups
- Solution: `sudo usermod -a -G dialout,tty $USER` then reboot

**Device Busy:**
- Arduino Serial Monitor is open
- Another Python script is running
- Solution: Close all other programs accessing the port

**No Response from Arduino:**
- Missing 2-second delay in Python or Arduino
- Baud rate mismatch
- Wrong serial port (`/dev/ttyACM0` vs `/dev/ttyUSB0`)

**Garbled Messages:**
- Baud rate mismatch between Python and Arduino
- Missing or incorrect message delimiter
- Solution: Verify both use 9600 baud and `\n` delimiter
