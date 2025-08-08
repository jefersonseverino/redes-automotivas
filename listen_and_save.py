import can
import time

def listen_and_save(channel='can0', interface='socketcan', log_file='can.log'):
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
        messages_interval = {}
        with open('can_log.csv', 'w', newline='\n') as file:
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
                    row = f"{hex(msg.arbitration_id)},{msg.dlc},{payload},{interval}\n"
                    file.write(row)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    listen_and_save(channel='can0', interface='socketcan', log_file='can.log')