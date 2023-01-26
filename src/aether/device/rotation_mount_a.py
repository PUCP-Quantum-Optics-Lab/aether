from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from aether.device.responses import DeviceInformation


class RotationMount:
    serial: Serial
    address: str

    def __init__(self, port: str, address: str = "0", timeout: float = None):
        self.address = address
        self.serial = Serial(
            port=port,
            baudrate=9600,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=timeout,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            write_timeout=None,
            inter_byte_timeout=None,
            exclusive=True,
        )
    
    def _write_serial(self, command: str) -> None:
        self.serial.write(f"{self.address}{command}".encode())

    def get_information(self) -> DeviceInformation:
        self._write_serial("in")
        response = self.serial.read(33)
        return DeviceInformation(
            bi_positional_slider=response[3:5].decode("ascii"),
            serial_number=response[5:13].decode("ascii"),
            manufacturing_year=int(response[13:17].decode("ascii")),
            firmware_release=response[17:19].decode("ascii"),
            hardware_release=response[19:21],
            travel=response[21:25],
            pulses=response[25:33],
        )
    
    def get_position(self) -> int:
        self._write_serial("gp")
        response = self.serial.read(10)
        return 
