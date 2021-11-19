# native imports
import tkinter as tk

# third-party imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

# custom imports


class GraphCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.figure = Figure(
            figsize=(5.6, 4.8),
            dpi=100
        )

        self.placeholder_plot = self.figure.add_subplot(111)
        self.placeholder_plot.text(0.5, 0.5, "Use The Configuration\nOptions to Create a Plot", 
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

    def create_new_plot(self, selected_radio, app_name, res_name, uom_type):
        if selected_radio == 1:
            print(app_name)

        print(res_name)
        print(uom_type)

        print("------------------------")