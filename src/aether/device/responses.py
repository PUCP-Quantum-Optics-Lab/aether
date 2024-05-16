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


class DeviceStatus:
    code: int
    message: str

    def __init__(self, code: int):
        code_error = {
            0: "OK, no error",
            1: "Communication time out",
            2: "Mechanical time out",
            3: "Command error or not supported",
            4: "Value out of range",
            5: "Module isolated",
            6: "Module out of isolation",
            7: "Initializing error",
            8: "Thermal error",
            9: "Busy",
            10: "Sensor Error (May appear during self-test. If code persists there is an error)",
            11: "Motor Error (May appear during self-test. If code persists there is an error)",
            12: "Out of Range (e.g., stage has been instructed to move beyond its travel range).",
            13: "Over Current error",
        }
        self.code = code

        if code in code_error:
            self.message = code_error[code]
        else:
            self.message = "Reserved"
