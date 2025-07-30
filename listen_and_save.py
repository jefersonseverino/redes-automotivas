import can

def listen_and_save(interface='can0', canal='socketcan', log_file='can.log'):
    try:
        bus = can.interface.Bus(channel=interface, bustype=canal)
        log_writer = can.Logger(log_file)  
        for msg in bus:
            print(f"ID: {hex(msg.arbitration_id)}, DLC: {msg.dlc}, Data: {msg.data.hex()}")
            log_writer.on_message_received(msg)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    listen_and_save(interface='can0', canal='socketcan', log_file='can.log')
