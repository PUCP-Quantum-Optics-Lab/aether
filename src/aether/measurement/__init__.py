from datetime import datetime
from dataclasses import dataclass

@dataclass
class DeviceAtMeasurement:
	address: str
	angle: int

@dataclass
class Measurement:
	code: str
	start_time: datetime
	end_time: datetime
	devices: list[DeviceAtMeasurement]