import logging

class CodeBehindLogger(logging.Logger):
    def __init__(self, level=logging.ERROR):
        super().__init__("zipit:code_behind", level=level)


        self.__stream_handler = logging.StreamHandler()
        self.__steam_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        self.__stream_handler.setFormatter(format)

        self.addHandler(self.__stream_handler)
    
code_behind_logger = CodeBehindLogger(level=logging.DEBUG)
