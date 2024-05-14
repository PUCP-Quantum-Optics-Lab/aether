from device.rotation_mount_a import RotationMount


def main():
    coincidence_files = [
        { name: "", last_line: 0},
        { name: "", last_line: 0},
    ]
    for cf in coincidence_files:
        with open(cf, , encoding="utf-8") as f:
            lines = f.readlines()
            cf["last_line"] = len(lines)
            

    mount = RotationMount("/dev/ttyUSB0", "0")
    info = mount.get_position()
    print(info)
    mount.close()


if __name__ == "__main__":
    main()
