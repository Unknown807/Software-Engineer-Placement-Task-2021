# native imports
import tkinter as tk
import pickle as pk

# third-party imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

# custom imports


class GraphCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_plot = None

        self.figure = Figure(
            figsize=(5.6, 4.8),
            dpi=100
        )

        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8])

        self.axes.text(0.5, 0.5, "Use The Configuration\nOptions to Create a Plot", 
            verticalalignment="center", horizontalalignment="center",
            color="orange", fontsize=14)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master = parent
        )

        self.canvas.draw()
        
        self.toolbar = NavigationToolbar2Tk(
            self.canvas,
            parent
        )

        self.toolbar.update()

    def create_new_plot(self, selected_radio, selected_yaxis_radio, log_yaxis, res_name, uom_type):
        self.figure.delaxes(self.axes)
        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8])
        self.axes.tick_params(axis="x", labelrotation=45, labelsize=7)

        # for dates and bars are to be labelled with 'ServiceName'
        xaxis_vals = []
        xaxis_vals_lbls = []

        # cost/consumption of resource
        yaxis_vals = []
        yaxis_type = "Cost" if selected_yaxis_radio == 1 else "ConsumedQuantity"
        
        filename = "application" if selected_radio == 1 else "resource"
    
        with open(filename+"_data.p", "rb") as lfile:
            data = pk.load(lfile)

        for item in data:
            if item["ServiceName"] == res_name:
                if item["UnitOfMeasure"] == uom_type:
                    xaxis_vals_lbls.append(item["ServiceName"])
                    xaxis_vals.append(item["Date"])
                    yaxis_vals.append(float(item[yaxis_type]))

        if log_yaxis:
            self.axes.set_yscale("log")
        
        self.current_plot = self.axes.bar(xaxis_vals, yaxis_vals, color="cornflowerblue")

        self.canvas.draw()
        self.toolbar.update()
        