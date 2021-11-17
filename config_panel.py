# native imports
import tkinter as tk
from tkinter import messagebox

# third-party imports
import Pmw as pmw

# custom imports
from api_utils import requestAPI

class ConfigPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # since the list of applications and resources is short
        # theres no problem storing it in memory
        self.app_names = requestAPI("applications")
        self.app_res_names = []

        self.res_names = requestAPI("resources")

        # to store radio buttons for applications/resources data
        self.data_type_frame = tk.LabelFrame(self, text="View data for:")

        self.radio_var = tk.IntVar()
        self.app_radio = tk.Radiobutton(
            self.data_type_frame,
            text="Applications",
            variable=self.radio_var,
            value=1,
            command = self.set_config_options
        )

        self.res_radio = tk.Radiobutton(
            self.data_type_frame,
            text="Resources",
            variable=self.radio_var,
            value=2,
            command = self.set_config_options
        )

        self.app_radio.pack(side="top", anchor="w")
        self.res_radio.pack(side="top", anchor="w")

        # to configure options such as serviceName and UnitOfMeasurement
        self.config_options_frame = tk.LabelFrame(self, text="Configuration Options:")

        self.application_name_dropdown = pmw.ComboBox(
            self.config_options_frame,
            label_text="Application Name",
            labelpos="nw",
            scrolledlist_items=self.app_names,
            selectioncommand=self.select_application
        )

        self.resources_name_dropdown = pmw.ComboBox(
            self.config_options_frame,
            label_text="Resource Name",
            labelpos="nw",
            scrolledlist_items=self.res_names,
            selectioncommand=self.select_resource
        )

        self.uom_name_dropdown = pmw.ComboBox(self.config_options_frame)

        self.application_name_dropdown.component("entryfield_entry").configure(
            state="disabled",
            disabledbackground="white",
            disabledforeground="black"
        )

        self.resources_name_dropdown.component("entryfield_entry").configure(
            state="disabled",
            disabledbackground="white",
            disabledforeground="black"
        )

        self.uom_name_dropdown.component("entryfield_entry").configure(
            state="disabled",
            disabledbackground="white",
            disabledforeground="black"
        )

        self.application_name_dropdown.pack(side="top", pady=5)
        self.resources_name_dropdown.pack(side="top")
        self.uom_name_dropdown.pack(side="top", pady=5)

        # packing relevant frames
        self.data_type_frame.pack(side="top", fill="both", pady=5)
        self.config_options_frame.pack(side="top", fill="both", expand=True)
        
        self.radio_var.set(1)
        self.set_config_options()

    def set_config_options(self):
        selected_radio = self.radio_var.get()
        self.reset_configs(selected_radio)

        if selected_radio == 1:
            self.application_name_dropdown.pack(side="top", anchor="w", pady=5)
        else:
            self.application_name_dropdown.pack_forget()

    def select_application(self):
        data = requestAPI("applications/"+self.application_name_dropdown.get())
        

    def select_resource(self):
        pass

    def create_new_plot(self):
        pass

    def reset_configs(self, selected_radio):
        if selected_radio == 1:
            self.application_name_dropdown.selectitem(self.app_names[0])
        
        self.resources_name_dropdown.selectitem(self.res_names[0])