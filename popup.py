import customtkinter
import webbrowser
from time import sleep


class PopUp(customtkinter.CTk):
    def __init__(self, job: dict):
        super().__init__()

        self.title("Job Status Update")
        self.geometry("300x100")
        self.iconbitmap("pliops64.ico")
        self.link = job['job_link']
        self.status = job['job_status']

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.popup_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.popup_frame.grid(row=0, column=0, sticky="nsew")
        self.popup_frame.rowconfigure(0, weight=1)
        self.popup_frame.columnconfigure(3, weight=1)

        self.popup_type_label = customtkinter.CTkLabel(self.popup_frame, text=f"Job - {job['job_type']}",
                                                       compound="center")
        self.popup_type_label.grid(row=0, column=0, padx=(10, 0), pady=0, sticky="nsw")

        self.popup_number_label = customtkinter.CTkLabel(self.popup_frame, text=f"{job['job_number']}",
                                                         compound="center",
                                                         font=customtkinter.CTkFont(size=12, weight="bold"))
        self.popup_number_label.grid(row=0, column=1, padx=10, pady=0, sticky="nsw")

        self.popup_status_label = customtkinter.CTkLabel(self.popup_frame, text=f"{job['job_status']}",
                                                         compound="left", text_color=self.status_color(),
                                                         font=customtkinter.CTkFont(size=12, weight="bold", ))
        self.popup_status_label.grid(row=0, column=2, padx=0, pady=0, sticky="nse")

        self.popup_link = customtkinter.CTkButton(self.popup_frame, height=30, text="Go To Job",
                                                  corner_radius=10, command=self.openweb)
        self.popup_link.grid(row=1, column=0, columnspan=3, padx=0, pady=(0, 20), sticky="s")

    def status_color(self):
        if self.status == "SUCCESS":
            return '#00FF37'
        if self.status == "FAILURE":
            return '#FF0004'
        if self.status == "ABORTED":
            return '#FFB200'

    def openweb(self):
        webbrowser.open(self.link, new=1)

    # TODO: create the popup as a sub-window os described in:
    # https://pythonprogramming.altervista.org/how-to-create-multiple-windows-with-tkinter-made-by-chat-gpt/

    # def show_popup(self):
    #     new_popup =


if __name__ == "__main__":
    job_dict1 = {'job_type': "request_runner",
                 'job_number': "1234321",
                 'job_status': "SUCCESS",
                 'job_link': "https://pl-jenkins01.pliops.ent:8443/job/test_driver/10025/consoleText"
                 }

    job_dict2 = {'job_type': "request_runner",
                 'job_number': "1234321",
                 'job_status': "FAILURE",
                 'job_link': "https://pl-jenkins01.pliops.ent:8443/job/test_driver/10025/consoleText"
                 }

    job_dict3 = {'job_type': "request_runner",
                 'job_number': "1234321",
                 'job_status': "ABORTED",
                 'job_link': "https://pl-jenkins01.pliops.ent:8443/job/test_driver/10025/consoleText"
                 }


    app1 = PopUp(job_dict1)
    app1.mainloop()
    app1.quit()
    sleep(5)

    # app2 = PopUp(job_dict2)
    # app2.mainloop()
    # app2.quit()
    # sleep(5)

    # app3 = PopUp(job_dict3)
    # app3.mainloop()
    # app3.quit()
