import can
import pandas as pd
from model import detect_anomaly
import time

def listen_and_detect():
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
        messages_interval = {}
        while True:
            for msg in bus:
                payload = "".join(["{:02X}".format(byte) for byte in msg.data])
                interval = 0
                if msg.arbitration_id not in messages_interval:
                    messages_interval[msg.arbitration_id] = time.time()
                else:
                    interval = time.time() - messages_interval[msg.arbitration_id]
                    messages_interval[msg.arbitration_id] = time.time()
                interval = round(interval, 2)
                row_data = {
                    'id': msg.arbitration_id,
                    'dlc': msg.dlc,
                    'payload': int(payload, 16),
                    'time': interval
                }
                anomalies = detect_anomaly(row_data)
                if not anomalies.empty:
                    print(f"from message {row_data}")
                    pass
                else:
                    print("No anomalies detected for message:", row_data)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    listen_and_detect()