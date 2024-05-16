from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from aether.device.responses import DeviceInformation, DeviceStatus
from aether.device.error import DeviceError
from typing import Union
from logging import getLogger
from time import sleep

logger = getLogger(__name__)

# https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_ID=12829
ENCODER_RESOLUTION = 143360


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

    def _angle_to_position(self, angle: int) -> str:
        return f"{int(angle / 360 * ENCODER_RESOLUTION):x}".upper()

    def _position_to_angle(self, travel: int) -> int:
        return round(travel / ENCODER_RESOLUTION * 360, 3) % 360

    def _handle_move(self, response: bytes) -> Union[DeviceStatus, int]:
        if response[1:3] == b"GS":
            return DeviceStatus(int(response[3:5]))
        elif response[1:3] == b"PO":
            try:
                position = int(response[3:11], 16)
            except:
                raise DeviceError("INVALID_POSITION", response)
            return self._position_to_angle(position)
        else:
            raise DeviceError("UNKNOWN_RESPONSE", response)

    def send(self, command: str) -> bytes:
        self.serial.write(f"{self.address}{command}".encode())
        return self.serial.readline()

    def get_information(self) -> DeviceInformation:
        response = self.send("in")
        return DeviceInformation(
            bi_positional_slider=response[3:5].decode("ascii"),
            serial_number=response[5:13].decode("ascii"),
            manufacturing_year=int(response[13:17].decode("ascii")),
            firmware_release=response[17:19].decode("ascii"),
            hardware_release=response[19:21],
            travel=response[21:25],
            pulses=response[25:33],
        )

    def get_status(self) -> DeviceStatus:
        response = self.send("gs")
        return DeviceStatus(int(response[3:5]))

    def get_position(self) -> int:
        res = self.send("gp")

        if res[1:3] != b"PO":
            raise DeviceError("UNKNOWN_RESPONSE", res)

        try:
            position = int(res[3:11], 16)
        except:
            return 0
        return self._position_to_angle(position)

    def home(self, clockwise: bool = True) -> Union[DeviceStatus, int]:
        res = self.send("ho")
        return self._handle_move(res)

    def move_absolute(self, angle: int) -> Union[DeviceStatus, int]:
        pos = self._angle_to_position(angle).zfill(8)
        res = self.send(f"ma{pos}")
        return self._handle_move(res)

    def mock(self, angle: int):
        logger.info("Moving (ensured) mount %s to angle %s", self.address, angle)
        return

    def ensure_move(self, angle: int) -> None:
        logger.info("Moving (ensured) mount %s to angle %s", self.address, angle)

        wait_time = 2.0
        max_iterations = 10
        tolerance = 0.01

        current_angle = self.get_position()

        if abs(current_angle - angle) <= tolerance:
            logger.info("Device %s already at %s. No action done.", self.address, angle)
            return

        tries = 0

        while tries < max_iterations:
            current_angle = self.move_absolute(angle)

            sleep(wait_time)
            status = self.get_status()
            while status.code == 9:
                logger.info(
                    "Waiting on device %s. Its status is %s.",
                    self.address,
                    status.message,
                )
                sleep(wait_time)
                status = self.get_status()

            if type(current_angle) != int:
                current_angle = self.get_position()
            if abs(current_angle - angle) <= tolerance:
                logger.info(
                    "Device %s moved to angle %s. Requested angle was %s",
                    self.address,
                    current_angle,
                    angle,
                )
                return

            self.home()
            sleep(wait_time)

            tries += 1

        logger.info(
            "Failed to move device %s moved to angle %s. Device is at %s",
            self.address,
            angle,
            current_angle,
        )

    def close(self) -> None:
        self.serial.close()
