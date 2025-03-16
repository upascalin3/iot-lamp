import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import ttk
import time

# MQTT broker settings
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "/student_group/light_control"

# Global variable to track light state
light_state = "OFF"

# Tkinter window setup
root = tk.Tk()
root.title("IoT Light Control - Lighter")
root.geometry("300x400")
root.configure(bg='#f0f4f8')  # Light blue background

# Lighter canvas
canvas = tk.Canvas(root, width=200, height=300, bg='#f0f4f8', highlightthickness=0)
canvas.pack(pady=20)

# Draw a simple lighter shape (rectangle with flame)
lighter_body = canvas.create_rectangle(80, 150, 120, 300, fill='#d3d3d3', outline='black')
flame = canvas.create_oval(85, 130, 115, 160, fill='gray')  # Dim flame initially

# Status label
status_label = ttk.Label(root, text="Status: Light is OFF", font=('Arial', 12), foreground='#34495e')
status_label.pack(pady=10)

def update_lighter(state):
    global light_state
    light_state = state
    if state == "ON":
        canvas.itemconfig(flame, fill='#ffcc00', outline='#ffcc00')  # Bright yellow flame
        canvas.itemconfig(lighter_body, fill='#c0c0c0')  # Slightly brighter body
        status_label.config(text="Status: Light is ON")
    else:
        canvas.itemconfig(flame, fill='gray')  # Dim gray flame
        canvas.itemconfig(lighter_body, fill='#d3d3d3')  # Default body color
        status_label.config(text="Status: Light is OFF")
    root.update()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received: {message}")
    if message == "ON":
        update_lighter("ON")
    elif message == "OFF":
        update_lighter("OFF")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
print("Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)

# Start the loop
try:
    client.loop_start()  # Non-blocking loop
    root.mainloop()  # Keep the GUI running
except KeyboardInterrupt:
    print("\nDisconnecting from broker")
    client.disconnect()
    root.destroy()