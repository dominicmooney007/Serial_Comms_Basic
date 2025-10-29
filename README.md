# Quick Start Files

This folder contains all the code files you need for the Quick Start Guide.

---

## 📁 What's Inside

### Arduino Sketches (.ino files)

1. **arduino_receiver.ino** - Basic one-way communication
   - Arduino receives messages from Raspberry Pi
   - Displays messages in Serial Monitor
   - Use with: `test_serial.py`

2. **arduino_twoway.ino** - Two-way communication
   - Arduino receives messages and sends responses back
   - Echo/confirmation example
   - Use with: `test_twoway.py`

### Python Scripts (.py files)

1. **test_serial.py** - Basic message sender
   - Sends one message to Arduino
   - View result in Arduino Serial Monitor
   - Use with: `arduino_receiver.ino`

2. **test_twoway.py** - Interactive communication
   - Sends message and reads response
   - Demonstrates bidirectional communication
   - Use with: `arduino_twoway.ino`

---

## 🚀 Quick Start

### Basic One-Way Communication

**Step 1:** Upload Arduino sketch
1. Open Arduino IDE
2. Open `arduino_receiver.ino`
3. Select Board: Tools → Board → Arduino Uno
4. Select Port: Tools → Port → /dev/ttyACM0
5. Click Upload (→ button)

**Step 2:** Run Python script
```bash
cd quick_start_files
python3 test_serial.py
```

**Step 3:** View results
1. Open Arduino IDE Serial Monitor
2. Set baud rate to 9600
3. You should see: "Received: Hello from Raspberry Pi!"

---

### Two-Way Communication

**Step 1:** Upload Arduino sketch
1. Open Arduino IDE
2. Open `arduino_twoway.ino`
3. Upload to Arduino

**Step 2:** Run Python script
```bash
python3 test_twoway.py
```

**Expected output:**
```
Connecting to Arduino...
Sending: Hello Arduino!
Waiting for response...
Arduino replied: Arduino received: Hello Arduino!
Communication complete!
```

---

## 🔧 Testing Your Setup

### Syntax Check (No Hardware Needed)

**Python:**
```bash
python3 -m py_compile test_serial.py
python3 -m py_compile test_twoway.py
```

**Arduino:**
Open sketches in Arduino IDE - it will check syntax automatically.

---

## 🐛 Troubleshooting

### "Permission denied" error
```bash
sudo chmod 666 /dev/ttyACM0
```

### "Port not found" error
```bash
# Check if Arduino is connected
lsusb | grep Arduino

# List available ports
ls /dev/ttyACM*
```

### "Port already in use"
- Close Arduino Serial Monitor before running Python scripts
- Only ONE program can use the serial port at a time

---

## 📝 Key Configuration

All files use these standard settings:

| Setting | Value |
|---------|-------|
| **Serial Port** | `/dev/ttyACM0` |
| **Baud Rate** | `9600` |
| **Message Delimiter** | Newline (`\n`) |
| **Timeout** | 1 second |

⚠️ **Both Arduino and Python must use the same baud rate!**

---

## 📚 File Relationships

```
One-Way Communication:
┌─────────────────────┐         ┌─────────────────────┐
│  test_serial.py     │ ──────> │ arduino_receiver.ino│
│  (Raspberry Pi)     │  USB    │     (Arduino)       │
└─────────────────────┘         └─────────────────────┘
                                         │
                                         ↓
                                 Serial Monitor
                                 (View messages)

Two-Way Communication:
┌─────────────────────┐  send   ┌─────────────────────┐
│  test_twoway.py     │ ──────> │  arduino_twoway.ino │
│  (Raspberry Pi)     │ <────── │     (Arduino)       │
└─────────────────────┘  reply  └─────────────────────┘
       │
       ↓
  Terminal Output
  (View response)
```

---

## 🎯 Next Steps

Once these examples work:

1. **Modify messages** - Change the text being sent
2. **Add more messages** - Send multiple messages in sequence
3. **Try experiments** - Use files in `../RPI-Arduino_serial/`
4. **Complete Lesson 0** - Read `../lesson_0_first_serial_message.md`
5. **Explore activities** - Check out `../student_user_guide.md`

---

## 💡 Code Templates

### Python Template
```python
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Arduino reset delay

ser.write("your message".encode())
ser.write(b'\n')

ser.close()
```

### Arduino Template
```cpp
void setup() {
  Serial.begin(9600);
  delay(2000);
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    // Process message
  }
}
```

---

**Version:** 1.0
**Last Updated:** October 2025
**Estimated Time:** 10 minutes to test all files
**Difficulty:** Beginner

**Happy coding! 🎉**
