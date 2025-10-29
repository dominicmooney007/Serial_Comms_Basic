# Servo Control Quick Start Guide
## Control a Servo Motor from Raspberry Pi 5 via Arduino

**Time Required:** 15-20 minutes
**Difficulty:** Beginner-Intermediate
**Prerequisites:** Basic serial communication working (complete parent quick start guide first)

---

## What You'll Build

By the end of this guide, you'll be able to:
- Control a servo motor's position (0-180 degrees) from your Raspberry Pi
- Send commands via serial communication
- Receive real-time feedback from the Arduino
- Use both interactive and command-line control modes

---

## Hardware You'll Need

| Component | Notes |
|-----------|-------|
| Raspberry Pi 5 | Or compatible model with Raspberry Pi OS |
| Arduino Uno R3 | Official or clone board |
| Servo Motor | SG90, MG90S, or any standard hobby servo (180° rotation) |
| USB A-B Cable | To connect Pi and Arduino |
| 3x Jumper Wires | Male-to-male or male-to-female for servo connections |

**Total Additional Cost:** ~$5 if you already have Pi and Arduino from the basic quick start

---

## Step 1: Wire the Servo Motor (5 minutes)

### Servo Wire Colors

Most hobby servos have three wires:
- **Signal** (Orange, Yellow, or White) - Control signal
- **VCC** (Red) - Power (+5V)
- **GND** (Brown or Black) - Ground

### Connections

Connect servo to Arduino:

```
Servo Motor              Arduino Uno R3
━━━━━━━━━━━━━━━━━━━     ━━━━━━━━━━━━━━━━━
Signal (Orange) ──────→  Pin 9 (Digital PWM)
VCC (Red)       ──────→  5V
GND (Brown)     ──────→  GND
```

### Important Notes

- **Pin 9** is critical - it's PWM-capable and specified in the code
- **Small servos** (like SG90) can be powered from Arduino 5V
- **Larger servos** may need an external 5V power supply with shared ground
- Ensure connections are secure - loose wires cause erratic behavior

---

## Step 2: Upload Arduino Sketch (5 minutes)

### On Raspberry Pi or Desktop Computer:

1. **Open Arduino IDE**
   ```bash
   arduino &
   ```

2. **Open the Servo Control Sketch**
   - File → Open
   - Navigate to: `Servo_Control/arduino_servo_control.ino`
   - Click **Open**

3. **Select Board**
   - Tools → Board → Arduino AVR Boards → **Arduino Uno**

4. **Select Port**
   - Tools → Port → **/dev/ttyACM0** (or available port)
   - If unsure, check: `ls /dev/ttyACM*`

5. **Upload Sketch**
   - Click the **Upload** button (→ arrow icon)
   - Wait for "Done uploading" message
   - **Expected time:** 10-15 seconds

---

## Step 3: Test Arduino (3 minutes)

Before running Python, verify the Arduino works independently:

1. **Open Serial Monitor**
   - Tools → Serial Monitor
   - Or press: **Ctrl+Shift+M**

2. **Configure Serial Monitor**
   - Set baud rate to: **9600**
   - Set line ending to: **Newline** or **Both NL & CR**

3. **Check Startup Messages**

   You should see:
   ```
   Arduino Servo Control Ready!
   Servo initialized at 90 degrees
   Send angles 0-180 to control servo position
   ```

4. **Test Servo Manually**

   Type these commands in the Serial Monitor:

   | Type | Expected Result |
   |------|----------------|
   | `90` | Servo moves to center position |
   | `0` | Servo moves to 0° (far left) |
   | `180` | Servo moves to 180° (far right) |
   | `45` | Servo moves to 45° |

   After each command, you should see:
   ```
   Servo moved to: 90 degrees
   ```

5. **Close Serial Monitor**

   **CRITICAL:** Close the Serial Monitor before running Python!
   - Only one program can access the serial port at a time

---

## Step 4: Run Python Script (2 minutes)

### Interactive Mode (Recommended)

1. **Navigate to Servo_Control folder**
   ```bash
   cd ~/Claude\ Code\ Projects/Serial_Comms_Basic/Servo_Control
   ```

2. **Run the script**
   ```bash
   python3 servo_control.py
   ```

3. **Expected Output**
   ```
   Connecting to Arduino on /dev/ttyACM0...
   Connected!

   === Interactive Servo Control ===
   Enter angles (0-180) to control the servo
   Type 'h' for help, 'q' to quit

   Arduino: Arduino Servo Control Ready!
   Arduino: Servo initialized at 90 degrees
   Arduino: Send angles 0-180 to control servo position

   Ready for commands!

   Enter command: _
   ```

---

## Step 5: Control the Servo (5 minutes)

### Try These Commands

In the interactive prompt:

1. **Center Position**
   ```
   Enter command: 90
   Moving servo to 90°...
     → Servo moved to: 90 degrees
   ```

2. **Full Left**
   ```
   Enter command: 0
   Moving servo to 0°...
     → Servo moved to: 0 degrees
   ```

3. **Full Right**
   ```
   Enter command: 180
   Moving servo to 180°...
     → Servo moved to: 180 degrees
   ```

4. **Custom Angle**
   ```
   Enter command: 45
   Moving servo to 45°...
     → Servo moved to: 45 degrees
   ```

5. **Quick Center**
   ```
   Enter command: c
   Moving to center position (90°)...
     → Servo moved to: 90 degrees
   ```

6. **Get Help**
   ```
   Enter command: h

   === Servo Control Help ===
   Commands:
     0-180        : Move servo to specified angle
     c, center    : Move servo to center position (90°)
     h, help      : Show this help message
     q, quit      : Exit program
   ```

7. **Exit Program**
   ```
   Enter command: q
   Exiting servo control...
   Connection closed. Goodbye!
   ```

---

## Alternative: Single Command Mode

For scripting or quick positioning:

```bash
# Move to 90 degrees and exit
python3 servo_control.py 90

# Move to 0 degrees
python3 servo_control.py 0

# Move to 180 degrees
python3 servo_control.py 180
```

**Expected Output:**
```
Connecting to Arduino on /dev/ttyACM0...
Connected!

Setting servo to 90°...
  → Servo moved to: 90 degrees
Command sent successfully!

Connection closed. Goodbye!
```

---

## Troubleshooting

### Problem: Permission Denied

**Error Message:**
```
✗ Error: Could not open serial port /dev/ttyACM0
Details: [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied
```

**Solution:**
```bash
# Quick fix (until reboot)
sudo chmod 666 /dev/ttyACM0

# Permanent fix
sudo usermod -a -G dialout $USER
sudo usermod -a -G tty $USER
sudo reboot  # Required!
```

---

### Problem: Port Not Found

**Error Message:**
```
✗ Error: Could not open serial port /dev/ttyACM0
Details: [Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory
```

**Solutions:**

1. **Check if Arduino is connected:**
   ```bash
   lsusb | grep Arduino
   ```

   Should show: `Arduino SA Arduino Uno` or similar

2. **Find the correct port:**
   ```bash
   ls /dev/ttyACM*
   ls /dev/ttyUSB*
   ```

   If Arduino is on different port (e.g., `/dev/ttyUSB0`), edit `servo_control.py`:
   ```python
   SERIAL_PORT = '/dev/ttyUSB0'  # Change line 29
   ```

---

### Problem: Port Already in Use

**Error Message:**
```
Details: [Errno 16] could not open port /dev/ttyACM0: [Errno 16] Device or resource busy
```

**Solutions:**

1. **Close Arduino Serial Monitor**
2. **Stop any other Python scripts:**
   ```bash
   # Find processes using the port
   lsof /dev/ttyACM0

   # Kill if needed
   kill <PID>
   ```

---

### Problem: Servo Not Moving

**Symptoms:** Commands are sent, confirmations received, but servo doesn't move

**Solutions:**

1. **Check Wiring**
   - Verify signal wire is on **Pin 9** (not another pin)
   - Ensure VCC and GND are properly connected
   - Check for loose connections

2. **Check Power**
   - Small servos: Arduino 5V should be sufficient
   - Large servos: May need external 5V power supply
   - Verify Arduino has power (LED should be on)

3. **Test Servo Hardware**
   - Try the servo on different pins (update code)
   - Test with a different servo if available
   - Check servo isn't mechanically jammed

---

### Problem: Servo Jitters or Moves Erratically

**Solutions:**

1. **Add Capacitor** (for power filtering)
   - 100-470µF capacitor across servo VCC and GND
   - Helps with power supply noise

2. **External Power Supply**
   - Use separate 5V power supply for servo
   - Connect grounds together (Arduino GND to external GND)
   - Arduino signal pin still connects to servo signal

3. **Check Connections**
   - Ensure all wires are firmly connected
   - Look for intermittent connections
   - Use quality jumper wires

---

### Problem: Invalid Angle Error

**Arduino Response:**
```
Error: Angle 270 out of range. Valid range: 0-180
```

**Solution:**
- Servo motors can only rotate 0-180 degrees
- Enter values within this range
- The Python script validates before sending, so this usually only appears in Serial Monitor

---

## What You've Learned

✅ **Hardware Integration**
- Wiring servo motors to microcontrollers
- Understanding PWM control signals
- Power requirements for actuators

✅ **Serial Protocol Design**
- Command/response patterns
- Input validation on both sides
- Error handling and user feedback

✅ **Interactive Control Systems**
- Building user-friendly interfaces
- Real-time hardware control
- Multiple control modes (interactive vs. command-line)

✅ **Debugging Skills**
- Testing components independently
- Identifying hardware vs. software issues
- Using Serial Monitor for diagnostics

---

## Next Steps

### Beginner Projects

1. **Sweep Pattern**
   - Modify Python script to sweep servo back and forth
   - Add loop that sends 0, 10, 20, ..., 180, 170, ..., 0

2. **Position Presets**
   - Create named positions: "left", "center", "right"
   - Map to 0, 90, 180 degrees

3. **Timed Movements**
   - Send sequences of angles with delays
   - Create choreographed movements

### Intermediate Projects

1. **Multiple Servos**
   - Control 2-3 servos on different pins
   - Modify protocol to specify pin number
   - Example: `"9:90"` (pin 9, angle 90)

2. **GUI Control**
   - Create graphical interface with sliders
   - Use Python Tkinter or PyQt5
   - Real-time position display

3. **Sensor Integration**
   - Add ultrasonic sensor to Arduino
   - Make servo respond to distance
   - Send sensor data back to Pi

### Advanced Projects

1. **Robotic Arm**
   - Use 2-3 servos to create an arm
   - Implement coordinate-to-angle conversion
   - Control end-effector position

2. **Web Interface**
   - Create Flask web server on Pi
   - Control servo from web browser
   - Add camera for visual feedback

3. **Game Controller**
   - Use joystick or gamepad input
   - Map analog stick to servo position
   - Create responsive control system

---

## Resources

### Code Files

- `arduino_servo_control.ino` - Arduino sketch with servo control
- `servo_control.py` - Python script for Pi control
- `README.md` - Complete documentation
- `../test_twoway.py` - Basic two-way communication example
- `../quick_start_guide.md` - Parent project guide

### Documentation

- Arduino Servo Library: https://www.arduino.cc/reference/en/libraries/servo/
- PySerial Documentation: https://pyserial.readthedocs.io/
- Raspberry Pi Serial: https://www.raspberrypi.com/documentation/

### Hardware Datasheets

- SG90 Servo: Common 9g micro servo (0-180°, 4.8-6V)
- MG90S Servo: Metal gear version of SG90
- Arduino Uno R3: ATmega328P microcontroller

---

## Checklist

Before you finish, make sure you've:

- [ ] Wired servo to Arduino Pin 9, 5V, and GND
- [ ] Uploaded arduino_servo_control.ino successfully
- [ ] Tested servo movement in Serial Monitor
- [ ] Run servo_control.py in interactive mode
- [ ] Moved servo to multiple positions (0, 90, 180)
- [ ] Tried both interactive and single command modes
- [ ] Understand the command protocol (angle + newline)
- [ ] Know how to troubleshoot common issues

---

## Summary

**What We Built:**
- Interactive servo control system using Raspberry Pi and Arduino
- Bidirectional serial communication with command/response protocol
- Real-time hardware control with validation and error handling

**Key Concepts:**
- PWM signals control servo position
- Serial commands encoded as text with delimiters
- Input validation prevents hardware damage
- Exclusive port access prevents conflicts

**Skills Gained:**
- Hardware wiring and connections
- Actuator control via microcontroller
- Interactive user interface design
- System integration and debugging

---

**Congratulations!** 🎉

You've successfully built a servo control system with Raspberry Pi and Arduino!

This project demonstrates the foundation of robotics and automation - controlling physical hardware through software. The same principles apply to robotic arms, camera gimbals, RC vehicles, and countless other applications.

**Ready to build something amazing?** Use this as a foundation for your next project!

---

**Version:** 1.0
**Last Updated:** October 2025
**Part of:** Serial_Comms_Basic Educational Project
**License:** Open source for educational use

**Questions or Issues?** Check the main README.md for additional troubleshooting and resources.
