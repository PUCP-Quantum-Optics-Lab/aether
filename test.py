from aether.device import RotationMount

rm1 = RotationMount("/dev/ttyUSB0", "0")
info = rm1.get_position()
print(info)

rm2 = RotationMount("/dev/ttyUSB0", "2")
info = rm2.get_position()
print(info)

rm1.close()
rm2.close()
