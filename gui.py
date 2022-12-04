import sys
import jenkins_jobs

from functools import partial
from time import sleep

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QLabel,
    QWidget,
)

LINE_HEIGHT = 20
LINK_WIDTH = 250
TYPE_WIDTH = 120
STATUS_WIDTH = 50
REMOVE_BUTTON_WIDTH = 60
GENERAL_BUTTON_WIDTH = 60
WINDOW_WIDTH = LINK_WIDTH + TYPE_WIDTH + STATUS_WIDTH + REMOVE_BUTTON_WIDTH


def remove_job_func(job_to_remove):
    print('removing job ' + job_to_remove)
    jenkins_jobs.remove_job_from_list(jobs, job_to_remove)


jobs = [{'link': '1.def', 'type': 'test_with_yaml', 'status': 'running'},
        {'link': '2.def', 'type': 'test_with_yaml', 'status': 'success'},
        {'link': '3.def', 'type': 'test_with_yaml', 'status': 'failure'},
        {'link': '3.def', 'type': 'test_with_yaml', 'status': 'failure'},
        {'link': '4.def', 'type': 'test_with_yaml', 'status': 'na'}]

app = QApplication([])
window = QWidget()
window.setWindowTitle("Jenkins Jobs Status")


def create_jobs_block(jobs):
    jobs_lines = {}

    for i in range(0, len(jobs)):
        jobs_lines[i] = {
            'link': QLabel(),
            'type': QLabel(),
            'status': QLabel(),
            'remove': QPushButton("Remove")
        }
        set_job_line_text(jobs_lines[i], jobs[i])
        jobs_lines[i]['link'].setFixedHeight(LINE_HEIGHT)
        jobs_lines[i]['link'].setFixedWidth(LINK_WIDTH)
        jobs_lines[i]['type'].setFixedHeight(LINE_HEIGHT)
        jobs_lines[i]['type'].setFixedWidth(TYPE_WIDTH)
        jobs_lines[i]['status'].setFixedHeight(LINE_HEIGHT)
        jobs_lines[i]['status'].setFixedWidth(STATUS_WIDTH)
        jobs_lines[i]['remove'].clicked.connect(partial(remove_job_func, i))
        jobs_lines[i]['remove'].setFixedHeight(LINE_HEIGHT)
        jobs_lines[i]['remove'].setFixedWidth(REMOVE_BUTTON_WIDTH)

    return jobs_lines


def set_job_line_text(job_line, job):
    job_line['link'].setText(job['link'])
    job_line['type'].setText(job['type'])
    job_line['status'].setText(job['status'])


def create_top_line():
    top_line = {
        'link_text': QLabel(),
        'type_text': QLabel(),
        'status_text': QLabel()
    }
    top_line['link_text'].setText(' Link ')
    top_line['link_text'].setFixedHeight(LINE_HEIGHT)
    top_line['type_text'].setText(' Type ')
    top_line['type_text'].setFixedHeight(LINE_HEIGHT)
    top_line['status_text'].setText(' Status ')
    top_line['status_text'].setFixedHeight(LINE_HEIGHT)

    return top_line


def create_bottom_line():
    bottom_line = {
        'add_button': QPushButton("Add Job"),
        'timer_text': QLabel(),
        'timer': QLabel(),
        'close_button': QPushButton("Close tool")
    }
    bottom_line['add_button'].setFixedHeight(2 * LINE_HEIGHT)
    bottom_line['add_button'].setFixedWidth(GENERAL_BUTTON_WIDTH)
    bottom_line['timer_text'].setText('Refresh in:')
    bottom_line['timer_text'].setFixedHeight(2 * LINE_HEIGHT)
    bottom_line['timer'].setText('0')
    bottom_line['timer'].setFixedHeight(2 * LINE_HEIGHT)
    bottom_line['timer'].setFixedWidth(GENERAL_BUTTON_WIDTH)
    bottom_line['close_button'].setFixedHeight(2 * LINE_HEIGHT)
    bottom_line['close_button'].setFixedWidth(GENERAL_BUTTON_WIDTH)
    bottom_line['close_button'].clicked.connect(gui_exit)

    return bottom_line


def create_layout(top_line, jobs_lines, bottom_line):
    layout = QGridLayout()

    layout.addWidget(top_line['link_text'], 0, 0)
    layout.addWidget(top_line['type_text'], 0, 1)
    layout.addWidget(top_line['status_text'], 0, 2, 1, 2)

    for i in range(0, len(jobs_lines)):
        layout.addWidget(jobs_lines[i]['link'], i + 1, 0)
        layout.addWidget(jobs_lines[i]['type'], i + 1, 1)
        layout.addWidget(jobs_lines[i]['status'], i + 1, 2)
        layout.addWidget(jobs_lines[i]['remove'], i + 1, 3)

    layout.addWidget(bottom_line['add_button'], len(jobs_lines) + 1, 0)
    layout.addWidget(bottom_line['timer_text'], len(jobs_lines) + 1, 1)
    layout.addWidget(bottom_line['timer'], len(jobs_lines) + 1, 2)
    layout.addWidget(bottom_line['close_button'], len(jobs_lines) + 1, 3)

    return layout


def show_refresh_timer(bottom_line):
    for i in range(0, 30):
        print("222")
        bottom_line['timer'].setText(str(30 - i))
        print("222")
        QApplication.processEvents()
        sleep(1)


def show_gui(gui_layout, jobs_lines):
    window.setLayout(gui_layout)
    window.resize(WINDOW_WIDTH, len(jobs_lines) * 20)
    window.show()

def gui_exit():
    sys.exit(app.exec())

# top_line = create_top_line()
# jobs_lines = create_jobs_block(jobs)
# bottom_line = create_bottom_line()
# gui_layout = create_layout(top_line, jobs_lines, bottom_line)
# show_gui(gui_layout, jobs_lines)


