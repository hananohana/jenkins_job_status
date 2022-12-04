import logging
import os
import sys
from threading import Lock
from threading import Thread
from time import sleep

import jenkins_jobs

from logger import set_logger, zip_log_files

write = sys.stdout.write

USER_INPUT = {'0': 'O', '1': '0'}
LOG_FILE = 'log_text'


def display(jobs, lock):
    while True:
        try:
            with lock:
                os.system('cls')
                jenkins_jobs.print_jobs_list(jobs)
                jenkins_jobs.update_jobs_statuses(jobs)
                os.system('cls')
                jenkins_jobs.print_jobs_list(jobs)
                jenkins_jobs.print_user_menu()

            for i in range(30):

                if USER_INPUT['0'] == 'q':
                    return None
                if USER_INPUT['1'] == '1':
                    USER_INPUT['1'] = '0'
                    break

                sleep(1)

        except IndentationError:
            sleep(3)
            continue

        except Exception as e:
            print(f"Caught unexpected exception {e}")
            print("Exception type is: ")
            print(type(e))
            print(e)
            break

    print("Exiting...")


def user_input(jobs, lock):
    while USER_INPUT['0'] != 'q':

        a = input(" ")
        b = 0

        with lock:
            if a == 'a':
                url = input("Add job:\n Insert job's Url:")
                description = input("Add a short description, or press 'Enter' to leave empty:")
                jenkins_jobs.add_job_to_list(jobs, url, description)
                a = 'O'
                b = '1'

            if a == 'r':
                job_num = input("Remove job:\nWhat job number to remove? ")
                jenkins_jobs.remove_job_from_list(jobs, int(job_num))
                a = 'O'
                b = '1'

            if a == 'u':
                job_num = input("Update job description:\nWhat job number to update? ")
                description = input("Add a short description, or press 'Enter' to leave empty:")
                jenkins_jobs.update_job_description(jobs_list=jobs, number=int(job_num), job_description=description)
                a = 'O'
                b = '1'

        USER_INPUT['0'] = a
        USER_INPUT['1'] = b


def main():
    logger = logging.getLogger(__name__)
    logger.info("START of logger - Main")

    jobs = {}
    jobs = load_from_file(jobs)

    lock = Lock()

    dis = Thread(target=display, args=(jobs, lock))
    u_input = Thread(target=user_input, args=(jobs, lock))

    dis.start()
    u_input.start()

    dis.join()
    u_input.join()

    print("Thanks for using this tool!")
    jenkins_jobs.save_jobs_to_file(jobs)


def load_from_file(jobs):
    if os.path.exists(jenkins_jobs.JOBS_FILE):
        jobs = jenkins_jobs.load_jobs_from_file()
    return jobs


if __name__ == '__main__':
    zip_log_files()
    set_logger(LOG_FILE)
    main()
