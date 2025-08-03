import can
import pandas as pd
from model import detect_anomaly

def listen_and_detect():
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        while True:
            for msg in bus:
                payload = "".join(["{:02X}".format(byte) for byte in msg.data])
                row_data = {
                    'id': int(str(msg.arbitration_id), 16),
                    'dlc': msg.dlc,
                    'payload': int(payload, 16)
                }
                anomalies = detect_anomaly(row_data)
                if not anomalies.empty:
                    print(f"Anomaly detected: {anomalies} from message {row_data}")
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    listen_and_detect()