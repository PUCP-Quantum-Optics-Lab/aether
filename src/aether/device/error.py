class DeviceError(Exception):
    code: str
    message: str
    response: bytes

    def __init__(self, code: str, response: bytes, message: str = None):
        self.code = code
        self.message = message
        self.response = response

    def __str__(self):
        return (
            f"{self.code}" if self.message is None else f"{self.code}: {self.message}"
        ) + f" - data: {self.response.decode('ascii')}"
