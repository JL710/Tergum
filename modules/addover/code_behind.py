import json
from pathlib import Path


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

def start():
    import time
    for i in range(0, 101, 10):
        yield {"event-message": f"event: {i}", "percentage": i, "finished": False if i != 100 else True}
        time.sleep(1)

