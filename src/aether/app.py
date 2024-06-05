import logging
from dataclasses import dataclass
from datetime import datetime
from json import dump, load
from logging import FileHandler, StreamHandler
from time import sleep
from typing import Dict

from aether.device import RotationMount, RotationMountCache
from aether.measurement import DeviceAtMeasurement, Measurement, MeasurementValues


@dataclass
class CoincidenceFile:
    name: str
    last_line: int


def main():
    logging.basicConfig(
        handlers=[StreamHandler(), FileHandler("aether.log")],
        format="[%(levelname)s] %(asctime)s >> %(message)s",
        level=logging.INFO,
    )

    with open("./config.json", encoding="utf-8") as f:
        config = load(f)

    coincidence_files: list[CoincidenceFile] = [
        CoincidenceFile(name=f, last_line=0) for f in config["coincidence_files"]
    ]

    cache = RotationMountCache(config["port"])

    measures: list[Measurement] = []

    for exp in config["experiments"]:
        a_len = set([len(d["angles"]) for d in exp["devices"]])
        if len(a_len) != 1:
            raise Exception(
                f"Angles on experiment {exp['name']} are not all the same length."
            )

        for i in range(len(exp["devices"][0]["angles"])):
            measurement = Measurement(
                code=exp["name"],
                devices=[],
                start_time=datetime.now(),
                end_time=datetime.now(),
                values=[],
            )

            for device in exp["devices"]:
                device_at_measurement = DeviceAtMeasurement(
                    address=device["address"], angle=device["angles"][i]
                )
                measurement.devices.append(device_at_measurement)
                mount = cache.get(device_at_measurement.address)
                mount.mock(device_at_measurement.angle)
                # mount.ensure_move(device_at_measurement.angle)

            for cf in coincidence_files:
                with open(cf.name, encoding="utf-8") as f:
                    lines = f.readlines()
                    cf.last_line = len(lines)

            measurement.start_time = datetime.now()
            sleep(exp["measurement_time"])

            for cf in coincidence_files:
                with open(cf.name, encoding="utf-8") as f:
                    lines = f.readlines()
                    measurement_value = MeasurementValues(
                        code=cf.name, values=lines[cf.last_line :]
                    )

                measurement.values.append(measurement_value)

            measurement.end_time = datetime.now()

            measures.append(measurement)

    cache.close_all()

    with open("./measurements.json", "w") as f:
        dump([m.json() for m in measures], f, indent="  ")


if __name__ == "__main__":
    main()
