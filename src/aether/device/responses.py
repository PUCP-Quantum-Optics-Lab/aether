from dataclasses import dataclass


@dataclass
class DeviceInformation:
    bi_positional_slider: str
    serial_number: str
    manufacturing_year: int
    firmware_release: str
    hardware_release: bytes
    travel: bytes
    pulses: bytes
