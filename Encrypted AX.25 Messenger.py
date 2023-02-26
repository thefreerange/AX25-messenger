import ax25
import serial
from Crypto.Cipher import AES

# Set up the encryption key
key = b'mysecretpassword' # replace with your own key
cipher = AES.new(key, AES.MODE_ECB)

# Define the baud rate and packet size
baud_rate = 9600 # replace with the desired baud rate
packet_size = 256 # replace with the desired packet size

# Convert the message to AX.25 protocol
callsign = "MYCALL" # replace with your own callsign
dest_callsign = "DEST" # replace with the destination callsign

# Set up the Bluetooth connection to the TNC
bluetooth_device = '/dev/rfcomm0' # replace with the appropriate device name for your system
bluetooth = serial.Serial(bluetooth_device, baud_rate)

# Send a packet over the Bluetooth connection
def send_packet(message):
    encrypted_message = cipher.encrypt(message.encode())
    packet = ax25.UI(destination=dest_callsign, source=callsign, info=encrypted_message)
    with ax25.Port(port=bluetooth_device) as port:
        port.send(packet)

# Listen for incoming packets and decrypt them
def receive_packets():
    with ax25.Port(port=bluetooth_device) as port:
        while True:
            packet = port.receive(packet_size)
            if packet:
                if packet.info:
                    decrypted_message = cipher.decrypt(packet.info).decode()
                    print("Received message: " + decrypted_message)

# Start listening for incoming packets in a separate thread
import threading
receiver_thread = threading.Thread(target=receive_packets)
receiver_thread.start()

# Send a message over the Bluetooth connection
message = "Hello, world!"
send_packet(message)

# Send additional messages while the receiver_thread is running
while receiver_thread.is_alive():
    message = input("Enter a message to send: ")
    send_packet(message)

