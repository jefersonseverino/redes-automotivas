import can

def listen_and_save(interface='can0', canal='socketcan', log_file='can.log'):
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        with open('can_log.csv', 'w', newline='\n') as file:
            while True:
                for msg in bus: 
                    payload = "".join(["{:02X}".format(byte) for byte in msg.data])
                    row = f"{hex(msg.arbitration_id)},{msg.dlc},{payload}\n"
                    file.write(row)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    listen_and_save(interface='can0', canal='socketcan', log_file='can.log')