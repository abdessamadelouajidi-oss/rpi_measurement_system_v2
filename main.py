"""Main application loop for the Raspberry Pi vibration measurement system."""

import time
import sys
import csv
from state_machine import StateMachine
from sensors import Accelerometer
from buttons import BeginButton, PowerButton
from leds import IdleLED, MeasuringLED
from config import (
    READING_INTERVAL,
    BEGIN_BUTTON_PIN,
    POWER_BUTTON_PIN,
    ACCELEROMETER_I2C_ADDRESS,
    IDLE_LED_PIN,
    MEASURING_LED_PIN,
    MEASURING_LED_BLINK_INTERVAL,
    CSV_OUTPUT_PATH
)


class MeasurementSystem:
    """Main vibration measurement system coordinator."""
    
    def __init__(self):
        """Initialize the measurement system."""
        print("=" * 60)
        print("Raspberry Pi Vibration Measurement System")
        print("=" * 60)
        print()
        
        # Initialize state machine
        self.state_machine = StateMachine()
        
        # Initialize sensor
        print("Initializing accelerometer...")
        self.accelerometer = Accelerometer(i2c_address=ACCELEROMETER_I2C_ADDRESS)
        print()
        
        # Initialize buttons
        print("Initializing buttons...")
        self.begin_button = BeginButton(pin=BEGIN_BUTTON_PIN)
        self.begin_button.set_callback(self.on_begin_button_pressed)
        
        self.power_button = PowerButton(pin=POWER_BUTTON_PIN)
        self.power_button.set_shutdown_callback(self.on_shutdown)
        print()
        
        # Initialize LEDs
        print("Initializing LEDs...")
        self.idle_led = IdleLED(pin=IDLE_LED_PIN)
        self.measuring_led = MeasuringLED(
            pin=MEASURING_LED_PIN,
            blink_interval=MEASURING_LED_BLINK_INTERVAL
        )
        self.idle_led.turn_on()  # Start with IDLE LED on
        print()
        
        self.running = True
        self.last_reading_time = 0
        self.readings = []
        self.csv_output_path = CSV_OUTPUT_PATH
    
    def on_begin_button_pressed(self):
        """Handle BEGIN button press - toggle measurement state."""
        self.state_machine.toggle_measurement()
        
        # Update LED states
        if self.state_machine.is_measuring():
            self.idle_led.turn_off()
            # Don't turn on measuring LED here - it will blink in the main loop
        else:
            self.measuring_led.turn_off()
            self.idle_led.turn_on()
    
    def on_shutdown(self):
        """Handle POWER button shutdown."""
        if self.state_machine.is_measuring():
            self.state_machine.stop_measurement()
        print("\nShutting down...")
        self.running = False
    
    def read_vibration(self):
        """Read accelerometer and print vibration data."""
        try:
            accel_data = self.accelerometer.read()
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.readings.append(
                {
                    "timestamp": timestamp,
                    "x": accel_data["x"],
                    "y": accel_data["y"],
                    "z": accel_data["z"],
                }
            )
            print(
                f"[{timestamp}] Vibration - "
                f"X={accel_data['x']:+.2f}m/s² "
                f"Y={accel_data['y']:+.2f}m/s² "
                f"Z={accel_data['z']:+.2f}m/s²"
            )
        except Exception as e:
            print(f"[ERROR] Failed to read accelerometer: {e}")
    
    def run(self):
        """Main application loop."""
        print("System ready. Press BEGIN button to start measuring.")
        print("Hold POWER button for 2+ seconds to shutdown.")
        print("-" * 60)
        print()
        
        try:
            while self.running:
                # Check button states
                self.begin_button.check_press()
                self.power_button.check_hold()
                
                # Update LEDs based on state
                if self.state_machine.is_measuring():
                    self.measuring_led.update()  # Blink the measuring LED
                
                # Read accelerometer if measuring
                current_time = time.time()
                if (
                    self.state_machine.is_measuring() and
                    current_time - self.last_reading_time >= READING_INTERVAL
                ):
                    self.read_vibration()
                    self.last_reading_time = current_time
                
                # Small sleep to avoid busy-waiting
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt received.")
            self.on_shutdown()
        
        finally:
            self.cleanup()

    def save_readings_to_csv(self):
        """Save collected readings to a CSV file after shutdown."""
        if not self.readings:
            print("[CSV] No readings to save.")
            return

        try:
            with open(self.csv_output_path, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "x", "y", "z"])
                writer.writeheader()
                writer.writerows(self.readings)
            print(f"[CSV] Saved {len(self.readings)} readings to {self.csv_output_path}")
        except Exception as e:
            print(f"[CSV] Failed to write CSV file: {e}")
    
    def cleanup(self):
        """Clean up GPIO and other resources."""
        print("Cleaning up...")
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
            print("GPIO cleanup complete.")
        except Exception:
            pass

        self.save_readings_to_csv()
        
        print("=" * 60)
        print("System shutdown complete.")
        print("=" * 60)


def main():
    """Entry point."""
    system = MeasurementSystem()
    system.run()


if __name__ == "__main__":
    main()
