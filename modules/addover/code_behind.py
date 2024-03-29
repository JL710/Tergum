import json
from pathlib import Path

import os


# data handeling
def load_data() -> dict:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    return data

def write_data(data: dict):
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)


# TODO: check profile decorator


# Profiles
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

def new_profile():
    profile_names = get_profile_names()
    i = 0
    while True:
        if not "new-profile" in profile_names:
            data = load_data()
            data["profiles"]["new-profile"] = {"target": str(Path.home()), "payload": []}
            break
        elif not f"new-profile-{i}" in profile_names:
            data = load_data()
            data["profiles"][f"new-profile-{i}"] = {"target": str(Path.home()), "payload": []}
            break
        else:
            i += 1
    write_data(data)

# Target
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

# payload
def get_payload(profile: str) -> list:
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

# command
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

# check cyclic
def check_cyclic(profile: str) -> bool:
    # get target
    target = get_target(profile)
    # get payload
    payload = get_payload(profile)
    # check
    for load in payload:
        if Path(load).is_file():
            if str(Path(load).parent) == str(target.parent):
                return True 
        elif str(Path(load)) in str(target):
            return True
        
    return False

# start / sync stuff / work stuff
def start(profile: str):
    # check if destination exists
    if not Path(get_target(profile)).exists():
        yield {"event-message": f"event: Destination {get_target(profile)} does not exist", "percentage": 100, "finished": True}
        return

    if len(get_payload(profile)) <= 0:
        yield {"event-message": f"event: No payload is available", "percentage": 100, "finished": True}
        return

    percent_factor = 100 / len(get_payload(profile))

    for index_payload, payload in enumerate(get_payload(profile)):
        # check if payload exists
        if not Path(payload).exists():
            yield {"event-message": f"event: Payload {payload} does not exist", "percentage": int(index_payload * percent_factor), "finished": False}
            continue
        
        yield {"event-message": f"Begin with: {payload}", "percentage": int(index_payload * percent_factor), "finished": False}

        destination = Path(get_target(profile) / Path(payload).name)

        if Path(payload).is_file() and not destination.is_file():
            with open(destination, "w") as file:
                pass # just to create the file if not already exists -> else xcopy will need user input

        command = get_command().replace("SOURCE", str(Path(payload)))
        command = command.replace("DESTINATION", str(destination))
        try:
            output = os.popen(command).read().decode('utf-8',errors='ignore')
        except UnicodeDecodeError:
            output = "!!!UnicodeDecodeError!!!" # FIXME: just not perfect solution
        yield {"event-message": f"xcopy output: {output}", "percentage": int(index_payload * percent_factor), "finished": False}
        
    yield {"event-message": f"Finished", "percentage": 100, "finished": True}



