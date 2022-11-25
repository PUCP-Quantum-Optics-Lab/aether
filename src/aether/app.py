from device.rotation_mount import open_serial, move_abs

def main():
    bus = open_serial("COM4")
    move_abs(bus, 1, 18)
    bus.close()

if __name__ == "__main__":
    main()
