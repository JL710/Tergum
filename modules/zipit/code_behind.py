from .db import DBManager
import typing
import time


def zipit(profile: str) -> dict:
    for i in range(1, 101):
        yield {"percentage": i, "message": f"message: {i}", "finished": False}
        time.sleep(0.1)
    yield {"percentage": 100, "message": f"message: finished", "finished": True}
