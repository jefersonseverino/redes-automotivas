import can
import pandas as pd
from model import detect_anomaly
import time

def listen_and_detect(channel='vcan0', interface='socketcan',):
    try:
        bus = can.interface.Bus(channel=channel, interface=interface)
        messages_interval = {}
        last_id = ""
        last_message_count = 0
        while True:
            for msg in bus:
                payload = "".join(["{:02X}".format(byte) for byte in msg.data])
                interval = 0
                if msg.arbitration_id not in messages_interval:
                    messages_interval[msg.arbitration_id] = time.time()
                else:
                    interval = time.time() - messages_interval[msg.arbitration_id]
                    messages_interval[msg.arbitration_id] = time.time()
                if msg.arbitration_id != last_id:
                    last_id = msg.arbitration_id
                    last_message_count = 1
                else:
                    last_message_count += 1
                interval = round(interval, 1)
                row_data = {
                    'id': msg.arbitration_id,
                    'dlc': msg.dlc,
                    'payload': int(payload, 16),
                    'time': interval,
                    'score': last_message_count
                }
                anomalies = detect_anomaly(row_data)
                if not anomalies.empty:
                  print(f"Detected anomalies on message {row_data}")
                else:
                  print("No anomalies detected for message:", row_data)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    listen_and_detect()