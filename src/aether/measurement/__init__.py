from datetime import datetime
from dataclasses import dataclass


@dataclass
class DeviceAtMeasurement:
    address: str
    angle: int

    def json(self) -> dict:
        return {"address": self.address, "angle": self.angle}


@dataclass
class MeasurementValues:
    code: str
    values: list[str]

    def json(self) -> dict:
        return {"code": self.code, "values": [int(l[:-2]) for l in self.values]}


@dataclass
class Measurement:
    code: str
    start_time: datetime
    end_time: datetime
    devices: list[DeviceAtMeasurement]
    values: list[MeasurementValues]

    def json(self) -> dict:
        return {
            "code": self.code,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "devices": [d.json() for d in self.devices],
            "values": [v.json() for v in self.values],
        }
