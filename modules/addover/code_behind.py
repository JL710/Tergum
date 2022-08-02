import json
from pathlib import Path

import os



def load_data() -> dict:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    return data

def write_data(data: dict):
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)


# TODO: check profile decorator


def get_target(profile: str) -> Path:
    path_string = load_data()["profiles"][profile]["target"]
    path = Path(path_string)
    if path_string == "":
        return Path.home()
    return path

def set_target(profile: str, path: str):
    data = load_data()
    data["profiles"][profile]["target"] = path
    write_data(data)

def get_profile_names() -> list:
    data = load_data()
    return list(data["profiles"].keys())

def delete_profile(profile: str):
    data = load_data()
    del data["profiles"][profile]
    write_data(data)

def rename_profile(old_profile: str, new_profile: str):
    data = load_data()
    if new_profile in data["profiles"]:
        raise Exception(f"Profile {new_profile} already exist")

    data["profiles"][new_profile] = data["profiles"][old_profile]
    del data["profiles"][old_profile]
    write_data(data)

def get_payloads(profile: str) -> list:
    data = load_data()
    return data["profiles"][profile]["payload"]

def set_payload(profile: str, payload: list):
    data = load_data()
    data["profiles"][profile]["payload"] = payload
    write_data(data)

def add_payload(profile: str, payload: str):
    data = load_data()
    if not payload in data["profiles"][profile]["payload"] and Path(payload).exists():
        data["profiles"][profile]["payload"].append(payload)
        write_data(data)

def remove_payload(profile: str, payload: str):
    data = load_data()
    if payload in data["profiles"][profile]["payload"]:
        data["profiles"][profile]["payload"].remove(payload)
        write_data(data)

def get_command() -> str:
    data = load_data()
    return data["command"]

def set_command(command: str) -> str:
    data = load_data()
    data["command"] = command
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def reset_command():
    data = load_data()
    data["command"] = data["default-command"]
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def start(profile: str):
    # check if destination exists
    if not Path(get_target(profile)).exists():
        yield {"event-message": f"event: Destination {get_target(profile)} does not exist", "percentage": 100, "finished": True}
        return

    percent_factor = 100 / len(get_payloads(profile))

    for index_payload, payload in enumerate(get_payloads(profile)):
        # check if payload exists
        if not Path(payload).exists():
            yield {"event-message": f"event: Payload {payload} does not exist", "percentage": int(index_payload * percent_factor), "finished": False}
            continue
        
        yield {"event-message": f"Begin with: {payload}", "percentage": int(index_payload * percent_factor), "finished": False}

        command = get_command().replace("SOURCE", str(Path(payload)))
        command = command.replace("DESTINATION", str(Path(get_target(profile) / Path(payload).name)))
        output = os.popen(command).read()
        yield {"event-message": f"xcopy output: {output}", "percentage": int(index_payload * percent_factor), "finished": False}
        
    yield {"event-message": f"Finished", "percentage": 100, "finished": True}



