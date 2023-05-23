import logging
import time


class Logger():
    def __init__(self):
        self.log = logging.getLogger()
        self.log.setLevel(level=logging.INFO)
        self.formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler = logging.FileHandler('./macro_downloader.log')
        self.fileHandler.setFormatter(self.formatter)
        self.log.addHandler(self.fileHandler)



if __name__ == '__main__':
    # logger = Logger()
    # logger.log.info("testtets")
    print(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())))