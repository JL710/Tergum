from .db import DBManager
import typing
import time
from pathlib import Path
import os
from .logger import code_behind_logger as log


def zipdir(zip_path: Path, local_path: Path, dir: Path):
    for root, dirs, files in os.walk(dir):
        for file in file:
            pass 
        # write to zip_path / local_path / file
        # write from root / file
            
        for dir in dirs:
            zipdir(local_path / dir, Path(dir))


def zipit(profile: str) -> dict:
    log.info(f'Start function zipit on profile "{profile}"')

    if not DBManager.profile_exists(profile):
        log.critical(f'zipit function -> Profile "{profile}" does not exist!')
        raise Exception(f'Profile "{profile}" does not exist!')

    # get some data from the database
    destination = DBManager.get_target(profile)
    included_cargo = DBManager.get_cargo(profile, include=True)
    excluded_cargo = DBManager.get_cargo(profile, include=False)

    # check the data
    if not destination:
        log.critical("zipit function -> Destination does not exist")
        raise Exception("Destination does not exist")

    log.debug(f"destination: {destination}")
    log.debug(f"included cargo: {included_cargo}")
    log.debug(f"excluded cargo: {excluded_cargo}")


    for i in range(1, 101):
        yield {"percentage": i, "message": f"message: {i}", "finished": False}
        time.sleep(0.1)
    yield {"percentage": 100, "message": f"message: finished", "finished": True}
