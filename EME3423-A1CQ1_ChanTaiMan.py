import serial
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import threading
import queue

# Configuration
SERIAL_PORT = 'COM3'  # Change to your Arduino port (e.g., '/dev/ttyUSB0' on Linux/Mac)
BAUD_RATE = 9600
WINDOW_NAME = 'Sensor Monitor with Webcam'

# Data queue for thread-safe communication
data_queue = queue.Queue()
temperatures = []
timestamps = []

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    ser = None


def read_serial():
    """Thread function to read serial data continuously"""
    while True:
        if ser and ser.is_open:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        temp = float(line)
                        data_queue.put(temp)j,
                    except ValueError:j,
                        pass
            except Exception as e:
                print(f"Serial read error: {e}")


# Start serial reading thread
if ser:
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    cap = None

# Create matplotlib figure for real-time plotting
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([], [], 'b-', linewidth=2)
ax.set_xlim(0, 60)  # Show last 60 seconds
ax.set_ylim(0, 50)  # Temperature range 0-50°C
ax.set_xlabel('Time (seconds ago)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Indoor Temperature')
ax.grid(True, alpha=0.3)

# Add text annotation for current temperature
current_temp_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                            fontsize=14, fontweight='bold', color='red')

last_temp = 0


def update_plot(frame):
    """Update matplotlib plot with new data"""
    global last_temp

    # Get all available data from queue
    while not data_queue.empty():
        try:
            temp = data_queue.get_nowait()
            temperatures.append(temp)
            timestamps.append(datetime.now())
            last_temp = temp

            # Keep only last 60 data points
            if len(temperatures) > 60:
                temperatures.pop(0)
                timestamps.pop(0)
        except queue.Empty:
            break

    if temperatures:
        # Create x-axis: seconds ago (0 = most recent)
        if len(temperatures) > 1:
            latest_time = timestamps[-1]
            x_data = [(latest_time - t).total_seconds() for t in timestamps]
            x_data = [max(0, x) for x in x_data]  # Ensure non-negative
            x_data.reverse()  # Most recent at right
            y_data = temperatures.copy()
            y_data.reverse()

            line.set_data(x_data, y_data)
            ax.set_xlim(max(0, max(x_data) - 60), max(x_data))

            # Update current temperature display
            current_temp_text.set_text(f'Current: {temperatures[-1]:.1f}°C')
        else:
            current_temp_text.set_text(f'Current: {temperatures[-1]:.1f}°C')

    return line, current_temp_text


def display_webcam_with_overlay():
    """Display webcam feed with temperature overlay"""
    while True:
        ret, frame = cap.read()
        if ret:
            # Add temperature overlay
            cv2.putText(frame, f"Indoor temperature is: {last_temp:.1f} degree C",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "EME3423-A1CQ1_ChanTaiMan",
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow(WINDOW_NAME, frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# Run webcam in a separate thread
webcam_thread = threading.Thread(target=display_webcam_with_overlay, daemon=True)
webcam_thread.start()

# Start matplotlib animation
print("Starting visualization... Press Ctrl+C to stop")
print("Press 'q' in webcam window to exit")

try:
    ani = FuncAnimation(fig, update_plot, interval=100, blit=False)
    plt.show(block=True)
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    # Cleanup
    if ser and ser.is_open:
        ser.close()
    if cap:
        cap.release()
    cv2.destroyAllWindows()