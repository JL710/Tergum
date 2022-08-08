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
            package_import = importlib.import_module(f"modules.{module_dir}")
            module_dict["widget"] = package_import.MainWidget()

            # load menu
            if package_import.Menu == None:
                module_dict["menu"] = None
            else:
                module_dict["menu"] = package_import.Menu(module_dict["widget"])
        
            modules.append(module_dict)
    return modules
