# TODO: add check for added job
# TODO: add show reached milestones in job run. e.g. all the steps in "blue ocean"
# TODO: add dealing with connection loss (<class 'requests.exceptions.ConnectionError'>)
# TODO: add show node number used for the job

import logging
import os
import sys
from queue import Queue
from threading import Lock, Thread
from time import sleep

import jenkins_jobs
from logger import set_logger, zip_log_files
from popup import PopUp

logger = logging.getLogger(__name__)

write = sys.stdout.write

USER_INPUT = {'0': 'O', '1': '0'}
LOG_FILE = 'log_text'
POP_UP_ENABLE = True


def update_and_display(jobs, queue, lock):
    global POP_UP_ENABLE
    a = 1
    while True:
        try:
            with lock:
                if a == 1:
                    os.system('cls')
                    jenkins_jobs.print_jobs_list(jobs_list=jobs)
                    a = 0
                jenkins_jobs.update_jobs_statuses(jobs_list=jobs, queue=queue, popup=POP_UP_ENABLE)
                os.system('cls')
                jenkins_jobs.print_jobs_list(jobs_list=jobs)
                jenkins_jobs.print_user_menu(POP_UP_ENABLE)

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
    global POP_UP_ENABLE
    while USER_INPUT['0'] != 'q':

        a = input(" ")
        b = 0

        with lock:
            if a == 'a':
                logger.info("Add New Job:")
                url = input("Add job:\n Insert job's Url:")
                description = input("\nAdd a short description, or press 'Enter' to leave empty:\nDescription: ")
                jenkins_jobs.add_job_to_list(jobs, url, description)
                a = 'O'
                b = '1'

            if a == 'r':
                logger.info("Remove Existing Job:")
                job_num = input("Remove job:\nWhat job number to remove? ")
                if int(job_num) < len(jobs) + 1 and int(job_num) > 0:
                    jenkins_jobs.remove_job_from_list(jobs, int(job_num))
                else:
                    print(f"No job number {job_num}.\nThere are {len(jobs)} jobs, listed (1 - {len(jobs)}).")
                    sleep(2)
                a = 'O'
                b = '1'

            if a == 'u':
                logger.info("Update Job Description:")
                job_num = input("Update job description:\nWhat job number to update? ")
                current_desc = jenkins_jobs.get_job_description(jobs_list=jobs, number=int(job_num))
                i = f"Current description of job {job_num} is:\n {current_desc}\n " \
                    f"Copy/Paste and edit or press 'Enter' to leave empty:"
                description = input(i)

                jenkins_jobs.update_job_description(jobs_list=jobs, number=int(job_num), job_description=description)
                a = 'O'
                b = '1'

            if a == 'p':
                logger.info("Changing pop-up settings:")
                if POP_UP_ENABLE:
                    print("Setting pop-up to - Disable. Will not show pop-up for job status change.")
                    POP_UP_ENABLE = False
                else:
                    print("Setting pop-up to - Enable. Will show pop-up for job status change.")
                    POP_UP_ENABLE = True
                a = '0'
                b = '1'

        USER_INPUT['0'] = a
        USER_INPUT['1'] = b


def show_popup(popup_queue, lock):
    global POP_UP_ENABLE

    while True:
        if USER_INPUT['0'] == 'q':
            return None

        job_dict = None
        try:
            job_dict = popup_queue.get(timeout=1)
        except Exception as e:
            logger.debug(f"Attempt to pull from queue got exception: {e}")
            sleep(5)

        logger.info(f"job dict : {job_dict}")

        if job_dict:
            popup = PopUp(job_dict)
            popup.mainloop()
            popup.quit()


def main():
    logger.info("START of logger - Main TEXT")

    jobs = {}
    jobs = load_from_file(jobs)

    lock = Lock()
    popup_queue = Queue()

    display_thread = Thread(target=update_and_display, args=(jobs, popup_queue, lock))
    popup_thread = Thread(target=show_popup, args=(popup_queue, lock))
    user_input_thread = Thread(target=user_input, args=(jobs, lock))

    display_thread.start()
    popup_thread.start()
    user_input_thread.start()

    display_thread.join()
    popup_thread.join()
    user_input_thread.join()

    jenkins_jobs.save_jobs_to_file(jobs)
    print("Thanks for using this tool!")


def load_from_file(jobs):
    if os.path.exists(jenkins_jobs.JOBS_FILE):
        jobs = jenkins_jobs.load_jobs_from_file(jenkins_jobs.JOBS_FILE)
    else:
        logger.info("jobs file does not exist, creating an empty file")
        jenkins_jobs.create_jobs_file()
        sleep(2)
    return jobs


if __name__ == '__main__':
    zip_log_files()
    set_logger(LOG_FILE)
    main()
