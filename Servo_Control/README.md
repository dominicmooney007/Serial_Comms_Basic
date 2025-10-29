# Servo Control Extension

Control a servo motor from your Raspberry Pi 5 using serial communication with Arduino Uno R3.

This project extends the basic serial communication examples to demonstrate practical hardware control through bidirectional serial commands.

---

## 📁 What's Inside

### Arduino Sketches (.ino files)

**arduino_servo_control.ino** - Servo motor control via serial commands
- Receives angle commands (0-180 degrees) from Raspberry Pi
- Controls servo position in real-time
- Validates input and provides error feedback
- Sends confirmation messages back to Pi
- Uses Arduino Servo library

### Python Scripts (.py files)

**servo_control.py** - Interactive servo control interface
- Interactive mode: Continuous servo control with command prompt
- Single command mode: Set angle and exit (command-line argument)
- Input validation and error handling
- Real-time feedback from Arduino
- Built-in help system

---

## 🔌 Hardware Requirements

### Components Needed

1. **Raspberry Pi 5** (or compatible model)
2. **Arduino Uno R3**
3. **Servo Motor** (e.g., SG90, MG90S, or any standard hobby servo)
   - Operating voltage: 4.8V - 6V
   - Rotation range: 0° - 180°
4. **USB A to B Cable** (for Pi-Arduino connection)
5. **Jumper Wires** (3x for servo connections)

### Wiring Diagram

Connect the servo motor to Arduino:

```
Servo Motor          Arduino Uno R3
━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━
Signal (Orange)  →  Pin 9 (PWM)
VCC (Red)        →  5V
GND (Brown)      →  GND
```

**Important Notes:**
- Pin 9 is a PWM-capable pin required for servo control
- Most small hobby servos (like SG90) can be powered from Arduino 5V
- For larger servos, use an external power supply with shared ground

---

## 🚀 Quick Start

### Step 1: Hardware Setup

1. Connect the servo motor to Arduino:
   - Signal wire (usually orange or yellow) → Pin 9
   - VCC wire (usually red) → 5V
   - GND wire (usually brown or black) → GND

2. Connect Arduino to Raspberry Pi via USB cable

### Step 2: Upload Arduino Sketch

1. Open Arduino IDE on your computer or Raspberry Pi
2. Open `arduino_servo_control.ino`
3. Select your board: **Tools → Board → Arduino Uno**
4. Select the port: **Tools → Port → /dev/ttyACM0** (or available port)
5. Click **Upload** (→ button)
6. Wait for "Done uploading" message

### Step 3: Verify Arduino Setup

1. Open **Serial Monitor** (Tools → Serial Monitor)
2. Set baud rate to **9600**
3. You should see:
   ```
   Arduino Servo Control Ready!
   Servo initialized at 90 degrees
   Send angles 0-180 to control servo position
   ```
4. Try sending angle values (e.g., `0`, `90`, `180`)
5. Watch the servo move!
6. **Close Serial Monitor before running Python script**

### Step 4: Run Python Script

**Interactive Mode** (recommended for testing):
```bash
cd Servo_Control
python3 servo_control.py
```

**Single Command Mode** (set angle and exit):
```bash
python3 servo_control.py 90    # Move to 90 degrees
python3 servo_control.py 0     # Move to 0 degrees
python3 servo_control.py 180   # Move to 180 degrees
```

### Step 5: Control the Servo

In interactive mode:
```
=== Interactive Servo Control ===
Enter angles (0-180) to control the servo
Type 'h' for help, 'q' to quit

Arduino: Arduino Servo Control Ready!
Arduino: Servo initialized at 90 degrees
Arduino: Send angles 0-180 to control servo position

Ready for commands!

Enter command: 90
Moving servo to 90°...
  → Servo moved to: 90 degrees

Enter command: 0
Moving servo to 0°...
  → Servo moved to: 0 degrees

Enter command: 180
Moving servo to 180°...
  → Servo moved to: 180 degrees

Enter command: q
Exiting servo control...
```

---

## 📝 Command Reference

### Interactive Mode Commands

| Command | Description | Example |
|---------|-------------|---------|
| `0-180` | Move servo to specified angle | `90` |
| `c` or `center` | Move to center position (90°) | `c` |
| `h` or `help` | Show help message | `h` |
| `q` or `quit` | Exit program | `q` |

### Command-Line Arguments

```bash
python3 servo_control.py [angle]     # Single command mode
python3 servo_control.py --help      # Show help
```

---

## 🔧 Configuration

### Standard Settings

All code uses these configurations:

| Setting | Value | Notes |
|---------|-------|-------|
| **Serial Port** | `/dev/ttyACM0` | May be `/dev/ttyUSB0` on some systems |
| **Baud Rate** | `9600` | Must match on both Arduino and Python |
| **Servo Pin** | `9` | PWM-capable pin on Arduino |
| **Angle Range** | `0-180` | Standard servo range |
| **Default Position** | `90` | Center position on startup |
| **Message Delimiter** | `\n` | Newline character |

### Changing the Serial Port

If your Arduino appears on a different port:

**In Python** (`servo_control.py`):
```python
SERIAL_PORT = '/dev/ttyUSB0'  # Change line 29
```

**Check available ports:**
```bash
ls /dev/tty{ACM,USB}*
```

---

## 🐛 Troubleshooting

### Servo Not Moving

**Problem:** Servo doesn't move when commands are sent

**Solutions:**
1. **Check wiring:**
   - Signal wire must be on Pin 9
   - Verify VCC and GND connections
2. **Check power:**
   - Small servos: Arduino 5V is sufficient
   - Large servos: May need external power supply
3. **Test with Serial Monitor:**
   - Upload sketch and open Serial Monitor
   - Send angles directly (e.g., `90`, `0`, `180`)
   - Verify servo moves before trying Python script

### Permission Denied Error

**Problem:** `SerialException: [Errno 13] Permission denied: '/dev/ttyACM0'`

**Solutions:**
```bash
# Temporary fix (until reboot)
sudo chmod 666 /dev/ttyACM0

# Permanent fix
sudo usermod -a -G dialout $USER
sudo usermod -a -G tty $USER
sudo reboot  # Required for groups to take effect
```

### Port Already in Use

**Problem:** `SerialException: [Errno 16] Device or resource busy`

**Solutions:**
1. Close Arduino Serial Monitor
2. Stop any other Python scripts using the port
3. Check for running processes:
   ```bash
   lsof /dev/ttyACM0
   ```

### Arduino Not Found

**Problem:** `SerialException: [Errno 2] No such file or directory: '/dev/ttyACM0'`

**Solutions:**
```bash
# Check if Arduino is connected
lsusb | grep Arduino

# List available serial ports
ls /dev/tty{ACM,USB}*

# May appear as /dev/ttyUSB0 instead
```

### Invalid Angle Error

**Problem:** Arduino returns error message for angle

**Solutions:**
- Verify angle is between 0 and 180
- Check that you're sending numbers, not text
- Ensure newline character is included (automatic in scripts)

### Servo Jitters or Behaves Erratically

**Solutions:**
1. **Check power supply:**
   - Servos under load may need external power
   - Add 100-470µF capacitor across servo power
2. **Add delays:**
   - Give servo time to reach position
   - In Python: `time.sleep(0.5)` after commands
3. **Check connections:**
   - Loose wires can cause intermittent operation
   - Ensure good contact on all connections

---

## 📚 How It Works

### Communication Flow

```
┌─────────────────────┐                 ┌─────────────────────┐
│   Raspberry Pi 5    │                 │   Arduino Uno R3    │
│                     │                 │                     │
│  servo_control.py   │    "90\n"       │ arduino_servo_      │
│                     │ ─────────────>  │   control.ino       │
│                     │                 │         │           │
│                     │                 │         ↓           │
│                     │   "Servo moved  │    Servo.write(90)  │
│   Displays result   │    to: 90°"     │         │           │
│         ↑           │ <─────────────  │         ↓           │
│         │           │                 │    ┌─────────┐      │
└─────────┼───────────┘                 │    │  Servo  │      │
          │                             │    │  Motor  │      │
          │                             │    └─────────┘      │
      User sees                         │   Physical movement │
    confirmation                        └─────────────────────┘
```

### Command Protocol

1. **User inputs angle** (0-180) in Python script
2. **Python validates** input and sends over serial: `"90\n"`
3. **Arduino receives** command and parses angle
4. **Arduino validates** angle range (0-180)
5. **Arduino moves servo** using `Servo.write(angle)`
6. **Arduino sends confirmation** back to Pi
7. **Python displays** confirmation to user

---

## 🎯 Project Extensions

Once you have this working, try these modifications:

### Beginner Extensions

1. **Sweep Pattern:**
   - Create a Python function that sweeps servo from 0° to 180° and back
   - Add speed control with delays between positions

2. **Preset Positions:**
   - Add named positions (e.g., "left", "center", "right")
   - Map to specific angles (0, 90, 180)

3. **Multiple Movements:**
   - Send sequence of angles from a list
   - Create choreographed servo movements

### Intermediate Extensions

1. **Multiple Servos:**
   - Control 2-3 servos on different pins
   - Modify protocol: `"pin:angle"` (e.g., `"9:90"`)

2. **Speed Control:**
   - Implement gradual movement between positions
   - Add speed parameter to commands

3. **Sensor Feedback:**
   - Add a sensor (ultrasonic, IR) to Arduino
   - Make servo respond to sensor readings
   - Send sensor data back to Pi

### Advanced Extensions

1. **GUI Control:**
   - Create a graphical interface with sliders
   - Use PyQt5 or Tkinter for GUI
   - Real-time servo position display

2. **Robotic Arm:**
   - Use multiple servos to create a 2-3 DOF arm
   - Implement inverse kinematics
   - Control end-effector position

3. **Web Interface:**
   - Create a Flask web server on Pi
   - Control servo from web browser
   - Add video streaming for visual feedback

---

## 💡 Code Structure

### Python Script Architecture

```python
# Configuration constants
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
MIN_ANGLE, MAX_ANGLE = 0, 180

# Main components
├── validate_angle()      # Input validation
├── send_angle()          # Send command and read response
├── interactive_mode()    # Continuous control loop
├── single_command_mode() # One-shot command
└── main()                # Entry point and connection setup
```

### Arduino Sketch Architecture

```cpp
// Configuration
const int SERVO_PIN = 9;
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

// Structure
├── setup()
│   ├── Serial.begin(9600)
│   ├── delay(2000)              // Critical stabilization
│   └── myServo.attach(SERVO_PIN)
│
└── loop()
    ├── Check Serial.available()
    ├── Read command with readStringUntil('\n')
    ├── Parse and validate angle
    ├── Move servo with write(angle)
    └── Send confirmation message
```

---

## 📖 Learning Objectives

By completing this project, you will learn:

1. **Hardware Control:**
   - How to control actuators (servo motors) digitally
   - PWM (Pulse Width Modulation) basics
   - Power requirements for motors

2. **Serial Communication:**
   - Command/response protocols
   - Input validation on both sides
   - Error handling and feedback

3. **System Integration:**
   - Coordinating hardware and software
   - Real-time control systems
   - User interface design

4. **Practical Skills:**
   - Wiring and circuit connections
   - Debugging hardware/software interactions
   - Building interactive control systems

---

## 🔗 Related Files

This project builds on the basic serial communication examples in the parent directory:

- `../test_serial.py` - Basic one-way communication
- `../test_twoway.py` - Bidirectional communication
- `../arduino_receiver.ino` - Basic Arduino receiver
- `../arduino_twoway.ino` - Arduino echo example
- `../quick_start_guide.md` - Complete setup guide

**Start here if you're new to serial communication!**

---

## 📋 Bill of Materials (BOM)

| Component | Quantity | Typical Cost | Notes |
|-----------|----------|--------------|-------|
| Raspberry Pi 5 | 1 | $60 | Or compatible model |
| Arduino Uno R3 | 1 | $25 | Official or clone |
| Servo Motor (SG90) | 1 | $3-5 | Standard hobby servo |
| USB A-B Cable | 1 | $3-5 | For Pi-Arduino connection |
| Jumper Wires | 3 | $2 | Male-to-male or male-to-female |

**Total Cost:** ~$95 (assuming you don't have Pi/Arduino)

**Note:** If you already completed the basic quick start guide, you only need to add the servo motor (~$5).

---

## 🆘 Getting Help

### Before Asking for Help

1. **Check wiring** - Most issues are connection problems
2. **Test with Serial Monitor** - Verify Arduino works independently
3. **Check permissions** - Serial port access is a common issue
4. **Read error messages** - They usually point to the problem

### Debugging Checklist

- [ ] Servo is properly wired to Pin 9, 5V, and GND
- [ ] USB cable is connected and Arduino has power
- [ ] Arduino sketch uploaded successfully
- [ ] Serial Monitor is closed before running Python
- [ ] User is in dialout and tty groups
- [ ] Serial port path is correct (`/dev/ttyACM0`)
- [ ] Baud rate is 9600 on both sides

---

**Version:** 1.0
**Last Updated:** October 2025
**Estimated Time:** 15-20 minutes (first time)
**Difficulty:** Beginner-Intermediate
**Prerequisites:** Complete basic serial communication quick start guide

**Happy building! 🤖⚙️**
