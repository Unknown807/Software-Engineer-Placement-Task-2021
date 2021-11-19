# native imports
import tkinter as tk
import pickle as pk

# third-party imports
import Pmw as pmw

# custom imports
from api_utils import requestAPI

class ConfigPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # since the list of applications and resources is short
        # theres no problem storing it in memory
        self.app_names = requestAPI("applications")
        
        self.app_res_names = []
        self.uomarr = []

        self.res_names = requestAPI("resources")

        # to store radio buttons for applications/resources data
        self.data_type_frame = tk.LabelFrame(self, text="Look at:")

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

        # view cost or consumption of resource/application's resources by some UnitOfMeasure

        self.yaxis_type_frame = tk.LabelFrame(self, text="View data for:")

        self.cc_var = tk.IntVar()
        self.cost_radio = tk.Radiobutton(
            self.yaxis_type_frame,
            text="Cost",
            variable=self.cc_var,
            value=1,
        )

        self.consumption_radio = tk.Radiobutton(
            self.yaxis_type_frame,
            text="Consumption",
            variable=self.cc_var,
            value=2,
        )

        self.app_radio.pack(side="top", anchor="w")
        self.res_radio.pack(side="top", anchor="w")
        self.cost_radio.pack(side="top", anchor="w")
        self.consumption_radio.pack(side="top", anchor="w")

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

        self.uom_name_dropdown = pmw.ComboBox(
            self.config_options_frame,
            label_text="Units of Measurement",
            labelpos="nw",
            scrolledlist_items=self.uomarr
        )

        # for styling purposes
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

        self.plot_button = tk.Button(
            self.config_options_frame,
            text="Create Plot",
            command=self.pass_config_to_root
        )

        self.application_name_dropdown.pack(side="top", pady=5)
        self.resources_name_dropdown.pack(side="top")
        self.uom_name_dropdown.pack(side="top", pady=5)
        self.plot_button.pack(side="top")

        # packing relevant frames
        self.data_type_frame.pack(side="top", fill="both")
        self.yaxis_type_frame.pack(side="top", fill="both", pady=5)
        self.config_options_frame.pack(side="top", fill="both", expand=True)
        
        self.radio_var.set(1)
        self.set_config_options()
        self.select_application(self.app_names[0])

    def set_config_options(self):
        selected_radio = self.radio_var.get()

        if selected_radio == 1:
            self.resources_name_dropdown.pack_forget()
            self.uom_name_dropdown.pack_forget()
            self.plot_button.pack_forget()

            self.application_name_dropdown.pack(side="top", pady=5)
            self.resources_name_dropdown.pack(side="top")
            self.uom_name_dropdown.pack(side="top", pady=5)
            self.plot_button.pack(side="top")

            self.application_name_dropdown.selectitem(self.app_names[0])
            self.select_application(self.app_names[0])
        else:
            self.application_name_dropdown.pack_forget()
            self.resources_name_dropdown.component("scrolledlist").setlist(self.res_names)
            self.resources_name_dropdown.selectitem(self.res_names[0])
            self.select_resource(self.res_names[0])

    def select_application(self, selected):
        self.app_res_names = ["All"]
        self.uomarr = []

        data = requestAPI("applications/"+selected)

        with open("application_data.p", "wb") as save_file:
            pk.dump(data, save_file, protocol=pk.DEFAULT_PROTOCOL)

        for resource in data:
            current_uom = resource["UnitOfMeasure"]
            current_name = resource["ServiceName"]

            if current_uom not in self.uomarr:
                self.uomarr.append(current_uom)
            
            if current_name not in self.app_res_names:
                self.app_res_names.append(current_name)

        # set resources_dropdown and uom dropdown data before select
        self.resources_name_dropdown.component("scrolledlist").setlist(self.app_res_names)
        self.uom_name_dropdown.component("scrolledlist").setlist(self.uomarr)

        self.resources_name_dropdown.selectitem(self.app_res_names[0])
        self.uom_name_dropdown.selectitem(self.uomarr[0])

    def select_resource(self, selected):
        if self.radio_var.get() == 1:
            return

        self.uomarr = []

        data = requestAPI("resources/"+selected)

        with open("resource_data.p", "wb") as save_file:
            pk.dump(data, save_file, protocol=pk.DEFAULT_PROTOCOL)

        for resource in data:
            current_uom = resource["UnitOfMeasure"]

            if current_uom not in self.uomarr:
                self.uomarr.append(current_uom)

        self.uom_name_dropdown.component("scrolledlist").setlist(self.uomarr)
        self.uom_name_dropdown.selectitem(self.uomarr[0])

    def pass_config_to_root(self):
        selected_radio = self.radio_var.get()
        selected_yaxis_radio = self.cc_var.get()

        app_name = self.application_name_dropdown.get()
        res_name = self.resources_name_dropdown.get()
        uom_type = self.uom_name_dropdown.get()

        self.parent.pass_config_to_graph(
            selected_radio,
            selected_yaxis_radio,
            app_name,
            res_name,
            uom_type
        )
        
        
        