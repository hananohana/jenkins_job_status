"""
job is a Jenkins job with the following details:
 * link
 * job's name
 * job's status

"""
import datetime
import json
import logging
import os.path
import pickle
import shutil
from time import sleep

import requests
import urllib3

JOBS_FILE = 'saved_jobs.pkl'
JOBS_FILE_BACKUP = 'saved_jobs.pkl.bck'
JOBS_FILE_DUMMY = 'saved_jobs_dummy.pkl'


##############
# Decorators #
##############

def p_func_enter_exit(func):
    def function_wrapper(*args, **kwargs):
        print("Before calling " + func.__name__)
        func(*args, **kwargs)
        print("After calling " + func.__name__)

    return function_wrapper


###########
# Classes #
###########

logger = logging.getLogger(__name__)


def is_job_finished(result: dict) -> bool:
    return True if result['result'] else False


class Jenkins:
    def __init__(self):
        with open('jenkins.txt', "r") as j:
            creds = j.read()
            json_creds = json.loads(creds)
        self.user = json_creds['user']
        self.token = json_creds['token']

    def update_user(self, user):
        self.user = user

    def update_token(self, token):
        self.token = token

    def fetch_page(self, url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_api_json = url + '/api/json'
        try:
            result = requests.post(url_api_json, auth=(self.user, self.token), verify=False)
            result_json = result.content.decode('utf8').replace("false", "False").replace("null", "None").replace(
                "true", "True")
            return result_json
        except ConnectionError as ce:
            logger.error(f"Got connection error exception {ce}. Either no internet connection or VPN is disconnected")
        except Exception as e:
            print(f"Caught unexpected exception {e}")
            print("Exception type is: ")
            print(type(e))
            print(e)


class JenkinsJob:
    def __init__(self, job_link='', job_desc='', job_node='', job_type='', job_number=0, job_status='na',
                 job_duration=0, job_start_time=0):
        self.job_link = job_link
        self.job_desc = job_desc
        self.job_node = job_node
        self.job_type = job_type
        self.job_number = job_number
        self.job_status = job_status
        self.job_duration = job_duration
        self.job_start_time = job_start_time

    def update_link(self, job_link: str):
        self.job_link = job_link

    def update_description(self, job_desc: str):
        self.job_desc = job_desc

    def update_type(self, page_dict: dict):
        self.job_type = page_dict['fullDisplayName'].split(" ")[0]

    def update_node(self, job_node: str):
        self.job_node = job_node

    def update_number(self, page_dict: dict):
        self.job_number = page_dict['number']

    def update_start_time(self, page_dict: dict):
        ts = page_dict['timestamp']
        job_start_time = datetime.datetime.fromtimestamp(ts)
        self.job_start_time = job_start_time

    def update_status(self, page_dict: dict):
        job_status = page_dict['result']
        self.job_status = job_status

    def fetch_job_page(self):
        jenkins = Jenkins()
        page_json = jenkins.fetch_page(self.job_link)
        return eval(page_json)  # eval : json -> dict

    def get_job_details_line(self):
        line1 = '{:64s} {:15s} {:9} {:10s}'.format(self.job_link, self.job_type, self.job_node, self.job_status)
        line2 = '{:94s}'.format(self.job_desc)
        return line1, line2

    def get_job_details_dict(self):
        return {'link': self.job_link, 'type': self.job_type, 'status': self.job_status}

    def update_job_details(self, queue, popup):
        page_dict = self.fetch_job_page()
        # logger.info(page_dict)
        self.update_type(page_dict)
        self.update_number(page_dict)
        full_display = page_dict['fullDisplayName'].split(" ")
        for item in full_display:
            if "Lab" in item:
                self.update_node(item.strip(","))
        if is_job_finished(page_dict):
            self.update_status(page_dict)
            if popup:
                job_dict = {'job_type': self.job_type,
                            'job_link': self.job_link,
                            'job_number': self.job_number,
                            'job_status': self.job_status
                            }
                queue.put(job_dict)
        else:
            self.update_status({'result': "Running..."})


def add_job_to_list(jobs_list, job_link, job_description):
    new_jenkins_job = JenkinsJob(job_link=job_link, job_desc=job_description)
    try:
        new_jenkins_job.fetch_job_page()
    except Exception as e:
        logger.error(f"During add job, caught exception - {e}")
        print(f"Job's details incorrect or job does not exist. Please check the job's address and try again")
        sleep(3)
        return
    jobs_list[len(jobs_list)] = new_jenkins_job
    logger.debug(f"Added job: {job_link} to list of jobs.")


def remove_job_from_list(job_list, number: int):
    job_to_remove = job_list[number - 1]
    logger.debug(f"Removing job: {str(job_to_remove)} from jobs list.")
    for i in range(number - 1, len(job_list) - 1):
        job_list[i] = job_list[i + 1]
    del job_list[len(job_list) - 1]
    logger.debug(f"Job: {str(job_to_remove)} was removed from jobs list.")
    logger.debug("Updated jobs list is: ")
    for i in job_list:
        logger.debug(str(i))


def get_job_description(jobs_list, number: int):
    return jobs_list[number - 1].job_desc


def update_job_description(jobs_list, number: int, job_description):
    logger.debug(f"Updating the description of job number {number} with new:\n {job_description}")
    jobs_list[number - 1].update_description(job_desc=job_description)
    logger.debug(f"Updated job details are: {jobs_list[number - 1]}")


def print_jobs_list(jobs_list):
    print(114 * "_")
    print("|-       " + '{:65s} {:15s} {:9} {:10s}'.format("Link", "Type", "Node", "Status") + " -|")
    print(114 * "-")
    if len(jobs_list) == 0:
        print("    No Jobs To Follow. Use (a) to add the first job...")
    for i in range(len(jobs_list)):
        job_details_line1, job_details_line2 = jobs_list[i].get_job_details_line()
        print("|- [" + '{:>2s}'.format(str(i + 1)) + "] - " + str(job_details_line1) + " -|")
        print("|- Description: " + str(job_details_line2) + "  -|")
    print(114 * "-")


def get_jobs_as_list_of_dicts(jobs_list):
    jobs_dict_list = {}
    for i in range(len(jobs_list)):
        jobs_dict_list[i] = jobs_list[i].get_job_details_dict()
    return jobs_dict_list


def update_jobs_statuses(jobs_list, queue, popup):
    for key, val in jobs_list.items():
        if val.job_status not in ["ABORTED", "SUCCESS", "FAILURE"]:
            val.update_job_details(queue=queue, popup=popup)


def save_jobs_to_file(the_jobs):
    if len(the_jobs) > 0:
        try:
            if os.path.exists(JOBS_FILE_BACKUP):
                os.remove(JOBS_FILE_BACKUP)
            shutil.copy(JOBS_FILE, JOBS_FILE_BACKUP)
            with open(JOBS_FILE, 'wb') as f:
                pickle.dump(the_jobs, f)
            logger.info(f"Jobs successfully saved to file {JOBS_FILE}")
        except Exception as e:
            logger.debug(e)
            logger.error("Couldn't backup jobs file..!")


def load_jobs_from_file(jobs_file):
    with open(jobs_file, 'rb') as f:
        logger.info("loading jobs from file")
        jobs = pickle.load(f)
        logger.info("jobs loaded successfully from file.")
        logger.info("jobs:")
        for i in jobs:
            logger.info(f"|- [{str(i)}] LINK: {str(jobs[i].job_link)} | DESCRIPTION: {str(jobs[i].job_desc)} -|")
        return jobs


def create_jobs_file():
    if not os.path.exists(JOBS_FILE):
        open(JOBS_FILE, "w").close()
        logger.info("jobs file created")


def print_user_menu(popup: bool):
    ena_dis = "enabled - Disable" if popup else "disabled - Enable"
    print("|- Use Input to:\n"
          "    (a)dd job\n"
          "    (r)emove job\n"
          "    (u)pdate job description\n"
          f"    (p)op-up is {ena_dis} pop-up\n"
          "    (q)uit...")
    return None
