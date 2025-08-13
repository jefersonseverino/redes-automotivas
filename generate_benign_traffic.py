import can
import time
import random
import threading

def send_messages(arbitration_id, messages, channel='vcan0', interface='socketcan'):
    try:
        bus = can.interface.Bus(channel=channel, interface=interface)
        while True:
            msg = random.choice(messages)
            bus.send(msg)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print(f"\nStopped sender for ID {hex(arbitration_id)}")
    except Exception as e:
        print(f"Error in sender {hex(arbitration_id)}: {e}")

if __name__ == "__main__":
    engine_start_on = can.Message(arbitration_id=0x1B8, data=[0x01], is_extended_id=False)
    engine_start_off = can.Message(arbitration_id=0x1B8, data=[0x00], is_extended_id=False)
    
    engine_status_on = can.Message(arbitration_id=0x19A, data=[0x01], is_extended_id=False)
    engine_status_off = can.Message(arbitration_id=0x19A, data=[0x00], is_extended_id=False)
    
    seat_belt_alarm_on = can.Message(arbitration_id=0x461, data=[0x01], is_extended_id=False)
    seat_belt_alarm_off = can.Message(arbitration_id=0x461, data=[0x00], is_extended_id=False)

    threading.Thread(target=send_messages, args=(0x1B8, [engine_start_on, engine_start_off]), daemon=True).start()
    threading.Thread(target=send_messages, args=(0x19A, [engine_status_on, engine_status_off]), daemon=True).start()
    threading.Thread(target=send_messages, args=(0x461, [seat_belt_alarm_on, seat_belt_alarm_off]), daemon=True).start()

    try:
        while True:
            #time.sleep(1) 
            pass
    except KeyboardInterrupt:
        print("\nFinished sending messages.")