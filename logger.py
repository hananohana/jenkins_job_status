import logging
import sys
from datetime import datetime
from zipfile import ZipFile
import os

LOGS_PATH = "./logs/"


def ensure_precondition():
    if not os.path.exists(LOGS_PATH):
        os.mkdir(LOGS_PATH)
    if not os.path.exists(LOGS_PATH + "old_logs/"):
        os.mkdir(LOGS_PATH + "old_logs/")


def zip_log_files():
    for file_name in os.listdir(LOGS_PATH):
        if file_name.endswith(".log"):
            zip_file_name = LOGS_PATH + "old_logs/" + file_name[:-4] + ".zip"
            full_file_name = LOGS_PATH + file_name
            with ZipFile(zip_file_name, 'w') as zip:
                zip.write(full_file_name)
            os.remove(LOGS_PATH + file_name)


def set_logger(log_file):
    ensure_precondition()
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                  '%d-%m-%Y %H:%M:%S')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.ERROR)
    stdout_handler.setFormatter(formatter)

    file_name_tail = str(datetime.now()).replace(":", "-").replace(" ", "_").split(".")[0]
    file_handler = logging.FileHandler(LOGS_PATH + log_file + "_" + file_name_tail + ".log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    # logger.addHandler(stdout_handler)

ensure_precondition()
