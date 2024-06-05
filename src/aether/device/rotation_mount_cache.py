from typing import Dict

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

from aether.device.rotation_mount import RotationMount


class RotationMountCache:
    cache: Dict[str, RotationMount]
    serial: Serial

    def __init__(self, port: str):
        self.cache = {}
        self.serial = Serial(
            port=port,
            baudrate=9600,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=None,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            write_timeout=None,
            inter_byte_timeout=None,
            exclusive=False,
        )

    def get(self, device_id: str) -> RotationMount:
        if device_id in self.cache:
            return self.cache[device_id]
        else:
            mount = RotationMount(self.serial, device_id)
            self.cache[device_id] = mount
            return mount

    def close_all(self) -> None:
        self.serial.close()
