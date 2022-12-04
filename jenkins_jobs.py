"""
job is a Jenkins job with the following details:
 * link
 * job's name
 * job's status

"""
import json
import logging
import pickle

import requests
import urllib3

JOBS_FILE = 'saved_jobs.pkl'


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
    def __init__(self, job_link='', job_desc='', job_type='', job_status='na'):
        self.job_link = job_link
        self.job_desc = job_desc
        self.job_type = job_type
        self.job_status = job_status

    def update_link(self, job_link: str):
        self.job_link = job_link

    def update_description(self, job_desc: str):
        self.job_desc = job_desc

    def update_type(self, page_dict: dict):
        job_type = page_dict['fullDisplayName'].split(" ")[0]
        self.job_type = job_type

    def update_status(self, page_dict: dict):
        job_status = page_dict['result']
        self.job_status = job_status

    def fetch_job_page(self):
        jenkins = Jenkins()
        page_json = jenkins.fetch_page(self.job_link)
        return eval(page_json)  # eval : json -> dict

    def get_job_details_line(self):
        line1 = '{:58s} {:25s} {:10s}'.format(self.job_link, self.job_type, self.job_status)
        line2 = '{:79s}'.format(self.job_desc)
        return line1, line2

    def get_job_details_dict(self):
        return {'link': self.job_link, 'type': self.job_type, 'status': self.job_status}

    def update_job_details(self):
        page_dict = self.fetch_job_page()
        self.update_type(page_dict)
        if is_job_finished(page_dict):
            self.update_status(page_dict)
        else:
            self.update_status({'result': "Running..."})


def add_job_to_list(jobs_list, job_link, job_description):
    jobs_list[len(jobs_list)] = JenkinsJob(job_link=job_link, job_desc=job_description)
    logger.debug("Added job: " + job_link + " to list of jobs.")


def remove_job_from_list(job_list, number: int):
    job_to_remove = job_list[number - 1]
    logger.debug("Removing job: " + str(job_to_remove) + " from jobs list.")
    for i in range(number - 1, len(job_list) - 1):
        job_list[i] = job_list[i + 1]
    del job_list[len(job_list) - 1]
    logger.debug("Job: " + str(job_to_remove) + " was removed from jobs list.")
    logger.debug("Updated jobs list is: " + str(job_list))


def update_job_description(jobs_list, number: int, job_description):
    logger.debug(f"Updating the description of job number {number} with new:\n {job_description}")
    jobs_list[number - 1].update_description(job_desc=job_description)
    logger.debug(f"Updated job details are: {jobs_list[number - 1]}")


def print_jobs_list(jobs_list):
    print(109 * "_")
    print("| -       " + '{:59s} {:25s} {:10s}'.format("Link", "Type", "Status") + " - |")
    print(109 * "-")
    for i in range(len(jobs_list)):
        job_details_line1, job_details_line2 = jobs_list[i].get_job_details_line()
        print("| - [" + '{:2s}'.format(str(i + 1)) + "] - " + str(job_details_line1) + " - |")
        print("| -  _description_ - " + str(job_details_line2) + "       - |")
    print(109 * "-")


def get_jobs_as_list_of_dicts(jobs_list):
    jobs_dict_list = {}
    for i in range(len(jobs_list)):
        jobs_dict_list[i] = jobs_list[i].get_job_details_dict()
    return jobs_dict_list


def update_jobs_statuses(jobs_list):
    for key, val in jobs_list.items():
        val.update_job_details()


def save_jobs_to_file(the_jobs):
    if len(the_jobs) > 0:
        with open(JOBS_FILE, 'wb') as f:
            pickle.dump(the_jobs, f)


def load_jobs_from_file():
    with open(JOBS_FILE, 'rb') as f:
        jobs = pickle.load(f)
        logger.debug(jobs)
        return jobs


def print_user_menu():
    print("|- Use Input to (a)dd, (r)emove job, (u)pdate job description or (q)uit... -|")
    return None
