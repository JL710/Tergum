import argparse
import os, shutil
from pathlib import Path
import json


# setup the main parser
parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest="subcommand_1", required=True)


# module parser
module_parser = subparser.add_parser("module", help='Module options. For more "module -h"')
module_subparser = module_parser.add_subparsers(dest="subcommand_2", required=True)

# module list parser
module_list_parser = module_subparser.add_parser("list", help="List all modules.")

# module create parser
module_create_parser = module_subparser.add_parser("create", help="Create a new empty module.")
module_create_parser.add_argument(
    "name",
    help="The name of the new module."
)

# module rm parser
module_rm_parser = module_subparser.add_parser("rm", help="Delete existing module.")
module_rm_parser.add_argument(
    "name",
    help="Name of the module."
)

# module reload
module_reload_parser = module_subparser.add_parser("reload", help="Reloads all modules into load_from_module.py")


# process args
args = parser.parse_args()
print(args)

if args.subcommand_1 == "module":
    if args.subcommand_2 == "list":
        print("{:<20}{:<20}".format("Name", "Title"))
        print("-"*40)
        for dir in [x for x in os.scandir("modules") if x.is_dir()]:
            with open(Path(dir, "settings.json"), "r") as f:
                name = json.load(f)["title"]    
            print("{:<20}{:<20}".format(str(dir.name), name))
    
    elif args.subcommand_2 == "create":
        if args.name in [x for x in os.scandir("modules") if x.is_dir()]:
            raise FileExistsError("Module exists already")

        module_dir = Path("modules", args.name)
        module_dir.mkdir() # create dir
        
        with open(module_dir / "module.py", "w") as f:
            f.write(
"""from PyQt5 import QtWidgets


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
            """)

        with open(module_dir / "settings.json", "w") as f:
            json.dump({"title": args.name}, f)

        with open(module_dir / "data.json", "w") as f:
            json.dump({}, f)

        with open(module_dir / "test.py", "w"):
            pass
    
    elif args.subcommand_2 == "rm":
        module_dir = Path("modules", args.name)
        if not os.path.isdir(module_dir):
            raise NotADirectoryError("The module does not exist.")
        shutil.rmtree(module_dir)

    elif args.subcommand_2 == "reload":
        # get list of modules
        module_names = os.listdir("modules")
        
        # create import strings
        string_pieces_import = []
        for module in module_names:
            string_pieces_import.append(f"from modules.{module} import MainWidget as {module}_widget")
        
        # create function strings
        string_pieces_function = []
        for module in module_names:
            string_pieces_function.append(f"widgets.append({module}_widget())")

        with open("load_from_module.py", "w") as f:
            for string in string_pieces_import:
                f.write(f"{string}\n")
            
            f.write("\ndef load_widgets() -> list:\n\twidgets = []\n\n")

            for string in string_pieces_function:
                f.write(f"\t{string}\n")

            f.write("\n\treturn widgets\n")


else:
    pass