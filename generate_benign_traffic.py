import can
import time
import random

def send_can_messages(channel='vcan0', interface='socketcan'):
    try:
        bus = can.interface.Bus(channel=channel, interface=interface)
        engine_start_on = can.Message(arbitration_id=0x1B8, data=[0x01], is_extended_id=False)
        engine_start_off = can.Message(arbitration_id=0x1B8, data=[0x00], is_extended_id=False)
        
        engine_status_on = can.Message(arbitration_id=0x19A, data=[0x01], is_extended_id=False)
        engine_status_off = can.Message(arbitration_id=0x19A, data=[0x00], is_extended_id=False)
        
        seat_belt_alarm_on = can.Message(arbitration_id=0x461, data=[0x01], is_extended_id=False)
        seat_belt_alarm_off = can.Message(arbitration_id=0x461, data=[0x00], is_extended_id=False)
        
        start_messages = [engine_start_on, engine_start_off]
        status_messages = [engine_status_on, engine_status_off]
        alarm_messages = [seat_belt_alarm_on, seat_belt_alarm_off]

        while True:
            start_selected = random.choice(start_messages)
            status_selected = random.choice(status_messages)
            alarm_selected = random.choice(alarm_messages)
            bus.send(start_selected)
            bus.send(status_selected)
            bus.send(alarm_selected)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_can_messages()