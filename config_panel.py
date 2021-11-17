# native imports
import tkinter as tk
from tkinter import messagebox

# third-party imports

# custom imports
from api_utils import get_app_or_res_list

class ConfigPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # since the list of applications and resources is short
        # theres no problem storing it in memory
        self.app_names = []
        self.res_names = []

        # to store radio buttons for applications/resources data
        self.data_type_frame = tk.LabelFrame(self, text="View data for:")

        self.radioVar = tk.IntVar()
        self.app_radio = tk.Radiobutton(
            self.data_type_frame,
            text="Applications",
            variable=self.radioVar,
            value=1,
            command = self.get_service_names
        )

        self.res_radio = tk.Radiobutton(
            self.data_type_frame,
            text="Resources",
            variable=self.radioVar,
            value=2,
            command = self.get_service_names
        )

        self.app_radio.pack(side="top", anchor="w")
        self.res_radio.pack(side="top", anchor="w")

        # to configure options such as serviceName and UnitOfMeasurement
        self.config_options_frame = tk.LabelFrame(self, text="Configuration Options:")

        # packing relevant frames
        self.data_type_frame.pack(side="top", fill="both", pady=5)
        self.config_options_frame.pack(side="top", fill="both", expand=True)
        
    def get_service_names(self):
        selected_radio = self.radioVar.get()

        if selected_radio == 1: #applications selected
            if len(self.app_names) != 0:
                print("already have apps")
                return
            path = "applications"

        elif selected_radio == 2: #resources selected
            if len(self.res_names) != 0:
                print("already have res")
                return
            path = "resources"

        names = get_app_or_res_list(path)
        
        if not names: # status code != 200
            messagebox.showerror("Error", "Check your internet connection or try again later")
            return

        if selected_radio == 1:
            self.app_names = names
        else:
            self.res_names = names

        self.display_config_options(selected_radio)
        
    def display_config_options(self, selected_radio):
        pass