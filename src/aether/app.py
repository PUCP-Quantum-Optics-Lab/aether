import logging
from json import dump, load
from logging import FileHandler, StreamHandler
from pathlib import Path
from configparser import ConfigParser
from requests import get

from serial.tools.list_ports import comports

from aether.job import execute_job

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        handlers=[StreamHandler(), FileHandler("aether.log")],
        format="[%(levelname)s] %(asctime)s >> %(message)s",
        level=logging.INFO,
    )

    logger.info("Available ports %s", [p.device for p in comports()])

    config_ini = ConfigParser()
    config_ini.read("config.ini")

    if config_ini["DEFAULT"]["env"] == "test":
        with Path("config.json").open() as f:
            config = load(f)

        measures = execute_job(config)

        logger.info("Saving measurements.")
        with Path("./measurements.json").open(mode="w") as f:
            dump([m.json() for m in measures], f, indent="  ")
    else:
        r = get(f"{config_ini['DEFAULT']['api_url']}/job/queue")
        print(r.status_code)


if __name__ == "__main__":
    main()
