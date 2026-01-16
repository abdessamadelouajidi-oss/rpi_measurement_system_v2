"""Configuration settings for the measurement system."""

# Button GPIO pins
BEGIN_BUTTON_PIN = 17      # GPIO 17 for BEGIN button
POWER_BUTTON_PIN = 27      # GPIO 27 for POWER button

# Sensor configuration
ACCELEROMETER_I2C_ADDRESS = 0x1C  # Default MMA8452 I2C address

# LED pins
IDLE_LED_PIN = 5        # GPIO 5 - lights up when in IDLE state
MEASURING_LED_PIN = 6   # GPIO 6 - blinks while measuring
MEASURING_LED_BLINK_INTERVAL = 0.5  # Blink every 0.5 seconds

# Measurement settings
READING_INTERVAL = 1.0  # Read vibration every 1.0 second while measuring
