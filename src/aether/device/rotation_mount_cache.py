from typing import Dict

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

from aether.device.rotation_mount import RotationMount


class RotationMountCache:
    mounts: Dict[str, RotationMount]
    connections: Dict[str, Serial]

    def __init__(self):
        self.mounts = {}
        self.connections = {}
    
    def connect(self, port_id: str, port: str) -> None:
        if port_id in self.connections:
            return

        self.connections[port_id] = None
        
        # self.connections[port_id] = Serial(
        #     port=port,
        #     baudrate=9600,
        #     bytesize=EIGHTBITS,
        #     parity=PARITY_NONE,
        #     stopbits=STOPBITS_ONE,
        #     timeout=None,
        #     xonxoff=False,
        #     rtscts=False,
        #     dsrdtr=False,
        #     write_timeout=None,
        #     inter_byte_timeout=None,
        #     exclusive=True,
        # )

    def get(self, port_id: str, device_id: str) -> RotationMount:
        key = f"{port_id}:{device_id}"
        if key in self.mounts:
            return self.mounts[key]
        else:
            mount = RotationMount(self.connections[port_id], device_id)
            self.mounts[key] = mount
            return mount

    def close_all(self) -> None:
        for m in self.mounts.values():
            m.close()
