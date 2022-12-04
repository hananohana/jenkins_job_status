import logging
import os
import sys
import gui

from time import sleep

import jenkins_jobs

from logger import set_logger

write = sys.stdout.write

USER_INPUT = {'0': 'O', '1': '0'}
LOG_FILE = 'log_gui'


def display(jobs):
    try:
        jobs_dict_list = jenkins_jobs.get_jobs_as_list_of_dicts(jobs)
        top_line = gui.create_top_line()
        jobs_lines = gui.create_jobs_block(jobs_dict_list)
        bottom_line = gui.create_bottom_line()
        gui_layout = gui.create_layout(top_line, jobs_lines, bottom_line)
        print("111")
        gui.show_gui(gui_layout, jobs_lines)
        print("111")

        jenkins_jobs.update_jobs_statuses(jobs)
        print("111")
        jobs_dict_list = jenkins_jobs.get_jobs_as_list_of_dicts(jobs)
        top_line = gui.create_top_line()
        jobs_lines = gui.create_jobs_block(jobs_dict_list)
        bottom_line = gui.create_bottom_line()
        gui_layout = gui.create_layout(top_line, jobs_lines, bottom_line)
        gui.show_gui(gui_layout, jobs_lines)
        print("111")
        gui.show_refresh_timer(bottom_line)
        print("111")

        while True:
            print("111")
            gui.show_refresh_timer(bottom_line)
            jenkins_jobs.update_jobs_statuses(jobs)
            jobs_dict_list = jenkins_jobs.get_jobs_as_list_of_dicts(jobs)
            jobs_lines = gui.create_jobs_block(jobs_dict_list)
            bottom_line = gui.create_bottom_line()
            gui_layout = gui.create_layout(top_line, jobs_lines, bottom_line)
            gui.show_gui(gui_layout, jobs_lines)




    except Exception as e:
        print(f"Caught unexpected exception {e}")
        print("Exception type is: ")
        print(type(e))
        print(e)

    print("Exiting...")


def main():
    logger = logging.getLogger(__name__)
    logger.info("START of logger - Main")

    jobs = {}
    jobs = load_from_file(jobs)

    display(jobs)

    #
    # lock = Lock()
    #
    # dis = Thread(target=display, args=(jobs, lock))
    # u_input = Thread(target=user_input, args=(jobs, lock))
    #
    # dis.start()
    # u_input.start()
    #
    # dis.join()
    # u_input.join()

    # print("Thanks for using this tool!")
    jenkins_jobs.save_jobs_to_file(jobs)


def load_from_file(jobs):
    if os.path.exists(jenkins_jobs.JOBS_FILE):
        jobs = jenkins_jobs.load_jobs_from_file()
    return jobs


if __name__ == '__main__':
    set_logger(LOG_FILE)
    main()
