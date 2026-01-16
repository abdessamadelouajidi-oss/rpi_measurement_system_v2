# Raspberry Pi Vibration Measurement System

A minimal, console-only vibration measurement system for Raspberry Pi with two buttons, one accelerometer sensor, and two status LEDs.

## Features

- **Two GPIO Buttons:**
  - **BEGIN Button (GPIO 17):** Press to toggle between IDLE and MEASURING states
  - **POWER Button (GPIO 27):** Hold for 2+ seconds to stop measurement and shutdown

- **One Sensor:**
  - **Accelerometer (I2C/MMA8452):** Measures vibration with x, y, z acceleration values

- **Two Status LEDs:**
  - **IDLE LED (GPIO 5):** Stays lit when in IDLE state
  - **MEASURING LED (GPIO 6):** Blinks while in MEASURING state

- **State Machine:** Simple two-state system (IDLE and MEASURING)

- **Console Output:** All vibration readings printed to console at 1-second intervals while measuring

## Project Structure

```
rpi_measurement_system/
├── main.py              # Main application entry point
├── state_machine.py     # Simple state machine (IDLE/MEASURING)
├── sensors.py           # Accelerometer class
├── buttons.py           # BeginButton and PowerButton classes
├── leds.py              # IdleLED and MeasuringLED classes
├── config.py            # Configuration settings (pins, intervals)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Hardware Configuration

### GPIO Pins
- **BEGIN Button:** GPIO 17
- **POWER Button:** GPIO 27
- **IDLE LED:** GPIO 5 (active HIGH)
- **MEASURING LED:** GPIO 6 (active HIGH)

### I2C Sensors
- **Accelerometer (MMA8452):** I2C address 0x1C

## Hardware Wiring

### Button Wiring
Both buttons use **internal pull-up resistors**, so no external resistors are needed.

**BEGIN Button (GPIO 17):**
- One end: GPIO 17 (Pin 11 on Raspberry Pi)
- Other end: GND (Ground - any GND pin)

**POWER Button (GPIO 27):**
- One end: GPIO 27 (Pin 13 on Raspberry Pi)
- Other end: GND (Ground - any GND pin)

### LED Wiring
Connect LEDs with 220Ω current-limiting resistor to protect GPIO pins:

**IDLE LED (GPIO 5):**
- GPIO 5 → 220Ω resistor → LED anode (longer leg)
- LED cathode (shorter leg) → GND

**MEASURING LED (GPIO 6):**
- GPIO 6 → 220Ω resistor → LED anode (longer leg)
- LED cathode (shorter leg) → GND

### Accelerometer (MMA8452) - I2C Connection
Connect to Raspberry Pi I2C bus (I2C-1 on most models):

| MMA8452 Pin | Raspberry Pi Pin | BCM GPIO |
|-------------|------------------|----------|
| VCC         | 3.3V Power       | -        |
| GND         | Ground (GND)     | -        |
| SDA         | GPIO 2           | 2        |
| SCL         | GPIO 3           | 3        |

**Note:** I2C address is 0x1C (can vary based on SD0/SA0 pin configuration)

### Raspberry Pi GPIO Header Reference
```
     3.3V │ 5V
     GPIO2 (SDA) │ 5V
     GPIO3 (SCL) │ GND
     GPIO4 │ GPIO17 (BEGIN Button)
     GND   │ GPIO27 (POWER Button)
           │ GPIO22
     3.3V  │ GPIO23
     GPIO24 │ GND
     GPIO25 │ GPIO18
     GND    │ GPIO15
     GPIO14 │ GPIO11
     GPIO5 (IDLE LED) │ GPIO10
     GPIO6 (MEASURING LED) │ GND
```

All GND connections can use any available ground pin on the Raspberry Pi.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Wire up your buttons and sensors according to the GPIO pin configuration above.

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Start Measurement:** Press the BEGIN button to transition from IDLE to MEASURING
2. **IDLE State:** IDLE LED is lit (stationary)
3. **MEASURING State:** MEASURING LED blinks while system reads vibration data every 1 second
4. **View Readings:** Vibration measurements are printed to console while measuring
5. **Stop Measurement:** Press the BEGIN button again to return to IDLE (IDLE LED lights up again)
6. **Shutdown:** Hold the POWER button for more than 2 seconds to stop measurement and shutdown

## Output Example

```
============================================================
Raspberry Pi Vibration Measurement System
============================================================

[ACCELEROMETER] Initialized on I2C address 0x1C
[BEGIN_BUTTON] Button initialized on GPIO 17
[POWER_BUTTON] Button initialized on GPIO 27
[IDLE_LED] LED initialized on GPIO 5
[MEASURING_LED] LED initialized on GPIO 6

System ready. Press BEGIN button to start measuring.
Hold POWER button for 2+ seconds to shutdown.
------------------------------------------------------------

[BEGIN_BUTTON] Pressed - toggling measurement
[STATE] Transitioned to MEASURING
[14:32:45] Vibration - X=+0.12m/s² Y=-0.08m/s² Z=+9.81m/s²
[14:32:46] Vibration - X=+0.11m/s² Y=-0.09m/s² Z=+9.80m/s²
[14:32:47] Vibration - X=+0.13m/s² Y=-0.07m/s² Z=+9.82m/s²
[BEGIN_BUTTON] Pressed - toggling measurement
[STATE] Transitioned to IDLE
```

## Notes

- All GPIO pins are configurable in `config.py`
- Sensor reading interval is configurable (default: 1.0 second)
- LED blink interval is configurable (default: 0.5 seconds)
- The system gracefully handles missing sensors with simulated data
- Button debouncing is implemented to prevent false triggers
- LEDs require 220Ω current-limiting resistors in series
- Press Ctrl+C to safely shutdown the application

## Dependencies

- `RPi.GPIO` - Raspberry Pi GPIO control
- `smbus-cffi` - I2C communication for sensors

The code is designed to run on a Raspberry Pi with Python 3.6+.
