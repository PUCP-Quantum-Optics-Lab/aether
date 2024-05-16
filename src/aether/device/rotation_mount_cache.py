from .rotation_mount import RotationMount
from typing import Dict


class RotationMountCache:
    cache: Dict[str, RotationMount]
    port: str

    def __init__(self, port: str):
        self.cache = {}
        self.port = port

    def get(self, device_id: str) -> RotationMount:
        if device_id in self.cache:
            return self.cache[device_id]
        else:
            mount = RotationMount(self.port, device_id)
            self.cache[device_id] = mount
            return mount

    def close_all(self) -> None:
        for v in self.cache.values():
            v.close()

        self.cache = {}
