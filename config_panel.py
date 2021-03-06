# native imports
import tkinter as tk
import pickle as pk
from tkinter import messagebox

# third-party imports
import Pmw as pmw

# custom imports
from api_utils import requestAPI

class ConfigPanel(tk.Frame):
    '''
    A tkinter frame placed on the left side of the screen, used to communicate with the API and get the data + user
    configurations of said data in order to plot it on the GraphCanvas and calculate min/max cost/consumption
    '''
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

        # functions which tell things about the data
        self.function_frame = tk.LabelFrame(self, text="Functions:")

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
            self.function_frame,
            text="Create Plot",
            command=self.pass_config_to_root
        )

        self.max_cc_button = tk.Button(
            self.function_frame,
            text="Max Cost/Consumption",
            command=self.get_highest_cost_or_consumption
        )

        self.min_cc_button = tk.Button(
            self.function_frame,
            text="Min Cost/Consumption",
            command=self.get_lowest_cost_or_consumption
        )

        # checkbox to choose whether to scale the y axis logarithmically

        self.logy_var = tk.IntVar()
        self.logy_checkbox = tk.Checkbutton(
            self.config_options_frame,
            text="Log Y Axis",
            variable=self.logy_var,
            onvalue=1,
            offvalue=0,
        )

        self.application_name_dropdown.pack(side="top", pady=5)
        self.resources_name_dropdown.pack(side="top")
        self.uom_name_dropdown.pack(side="top", pady=5)
        self.logy_checkbox.pack(side="top")

        self.plot_button.pack(side="top", pady=5)
        self.max_cc_button.pack(side="top")
        self.min_cc_button.pack(side="top", pady=5)

        # packing relevant frames
        self.data_type_frame.pack(side="top", fill="both")
        self.yaxis_type_frame.pack(side="top", fill="both", pady=5)
        self.config_options_frame.pack(side="top", fill="both", expand=True)
        self.function_frame.pack(side="top", fill="both", pady=5)
        
        # pick some default options
        self.radio_var.set(1)
        self.cc_var.set(1)
        self.set_config_options()
        self.select_application(self.app_names[0])

    def set_config_options(self):
        '''
        if you select applications or resources, some options should disappear as they only correspond to one or the other
        e.g there should be no applications dropdown if you're looking at /resources
        '''
        selected_radio = self.radio_var.get()

        if selected_radio == 1:
            self.resources_name_dropdown.pack_forget()
            self.uom_name_dropdown.pack_forget()
            self.logy_checkbox.pack_forget()

            self.application_name_dropdown.pack(side="top", pady=5)
            self.resources_name_dropdown.pack(side="top")
            self.uom_name_dropdown.pack(side="top", pady=5)
            self.logy_checkbox.pack(side="top")

            self.application_name_dropdown.selectitem(self.app_names[0])
            self.select_application(self.app_names[0])
        else:
            self.application_name_dropdown.pack_forget()
            self.resources_name_dropdown.component("scrolledlist").setlist(self.res_names)
            self.resources_name_dropdown.selectitem(self.res_names[0])
            self.select_resource(self.res_names[0])

    def select_application(self, selected):
        '''
        if you select an application from the dropdown, it will get data for it from the API and save it.
        It will then also alter other dropdowns, to show what resources the application has and all their
        respective units of measure
        '''
        self.app_res_names = []
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
        '''
        The same as select_application, but it just focuses on saving API data to a separate file
        '''
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
        '''
        When you choose to create a new graph plot, this method will pass all the necessary data to a method
        in the root object, 'pass_config_to_graph'.
        '''
        selected_radio = self.radio_var.get()
        selected_yaxis_radio = self.cc_var.get()
        log_yaxis = self.logy_var.get()

        res_name = self.resources_name_dropdown.get()
        uom_type = self.uom_name_dropdown.get()

        self.parent.pass_config_to_graph(
            selected_radio,
            selected_yaxis_radio,
            log_yaxis,
            res_name,
            uom_type
        )

    def get_cost_consumption_data(self):
        '''
        gets the file data according to the which radio buttons are selected and is shared by the min/max methods
        '''
        cost_or_consumption = "Cost" if self.cc_var.get() == 1 else "ConsumedQuantity"
        filename = "application" if self.radio_var.get() == 1 else "resource"
        with open(filename+"_data.p", "rb") as lfile:
            return (cost_or_consumption, pk.load(lfile))

    def get_highest_cost_or_consumption(self):
        '''
        Loops through and gets the highest cost/consumption from the data of the current resource or all
        resources of an application
        '''
        cost_or_consumption, data = self.get_cost_consumption_data()

        _max = 0
        res_name = "NONE FOUND"
        res_date = ""
        for item in data:
            val = float(item[cost_or_consumption])
            if val > _max:
                _max = val
                res_name = item["ServiceName"]
                res_date = item["Date"]
        
        msg = "The resource with the highest "+cost_or_consumption.lower()+" is "+res_name+", with "+str(_max)+" on the "+res_date
        messagebox.showinfo("Results", msg)

    def get_lowest_cost_or_consumption(self):
        '''
        Loops through and gets the lowest cost/consumption from the data of the current resource or all
        resources of an application
        '''
        cost_or_consumption, data = self.get_cost_consumption_data()

        _min = float(data[0][cost_or_consumption])
        res_name = data[0]["ServiceName"]
        res_date = data[0]["Date"]
        for item in data:
            val = float(item[cost_or_consumption])
            if val < _min:
                _min = val
                res_name = item["ServiceName"]
                res_date = item["Date"]

        msg = "The resource with the lowest "+cost_or_consumption.lower()+" is "+res_name+", with "+str(_min)+" on the "+res_date
        messagebox.showinfo("Results", msg)
        
        