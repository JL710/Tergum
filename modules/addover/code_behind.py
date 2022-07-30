import json
from pathlib import Path

import os



def load_target() -> Path:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        path_string = json.load(f)["Target"]     
    path = Path(path_string)
    if path_string == "":
        return Path.home()
    return path

def set_target(path: str):
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    data["Target"] = path
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def load_paylods() -> list:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    return data["payload"]

def set_payload(payload: list):
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    data["payload"] = payload
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def add_payload(payload: str):
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    if not payload in data["payload"] and Path(payload).is_dir():
        data["payload"].append(payload)
        with open(Path("modules", "addover", "data.json"), "w") as f:
            json.dump(data, f)

def remove_payload(payload: str):
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    if payload in data["payload"]:
        data["payload"].remove(payload)
        with open(Path("modules", "addover", "data.json"), "w") as f:
            json.dump(data, f)

def get_command() -> str:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    return data["command"]

def set_command(command: str) -> str:
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    data["command"] = command
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def reset_command():
    with open(Path("modules", "addover", "data.json"), "r") as f:
        data = json.load(f)
    data["command"] = data["default-command"]
    with open(Path("modules", "addover", "data.json"), "w") as f:
        json.dump(data, f)

def start():
    # check if destination exists
    if not Path(load_target()).exists():
        yield {"event-message": f"event: Destination {load_target()} does not exist", "percentage": 100, "finished": True}
        return

    percent_factor = 100 / len(load_paylods())

    for index_payload, payload in enumerate(load_paylods()):
        # check if payload exists
        if not Path(payload).exists():
            yield {"event-message": f"event: Payload {payload} does not exist", "percentage": int(index_payload * percent_factor), "finished": False}
            continue
        
        yield {"event-message": f"Begin with: {payload}", "percentage": int(index_payload * percent_factor), "finished": False}

        command = get_command().replace("SOURCE", str(Path(payload)))
        command = command.replace("DESTINATION", str(Path(load_target() / Path(payload).name)))
        output = os.popen(command).read()
        yield {"event-message": f"xcopy output: {output}", "percentage": int(index_payload * percent_factor), "finished": False}
        
    yield {"event-message": f"Finished", "percentage": 100, "finished": True}



