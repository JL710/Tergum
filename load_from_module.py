import os, importlib, json
from pathlib import Path


def load_modules() -> list:
    modules = []
    
    for module_dir in os.listdir("modules"):
        if module_dir != "__pycache__":

            module_dict = {"name": module_dir}

            # load title
            with open(Path("modules", module_dir, "settings.json"), "r") as f:
                module_dict["title"] = json.load(f)["title"]
            
            # load widget
            module_import = importlib.import_module(f"modules.{module_dir}.module")
            module_dict["widget"] = module_import.MainWidget()
        
        modules.append(module_dict)
    return modules
