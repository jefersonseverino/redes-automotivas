import can
import time

def listen_and_save(channel='vcan0', interface='socketcan', log_file='can.log'):
    try:
        bus = can.interface.Bus(channel=channel, interface=interface)
        messages_interval = {}
        last_id = ""
        last_message_count = 0
        with open('./data/can_log.csv', 'w', newline='\n') as file:
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
                    row = f"{hex(msg.arbitration_id)},{msg.dlc},{payload},{interval},{last_message_count},0\n"
                    file.write(row)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    listen_and_save(channel='vcan0', interface='socketcan', log_file='can.log')