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

        self.parent = parent

        self.figure = Figure(
            figsize=(5.6, 4.8),
            dpi=100
        )

        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8])

        #self.current_plot = self.figure.add_subplot(111)
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

    def create_new_plot(self, selected_radio, selected_yaxis_radio, app_name, res_name, uom_type):
        print(selected_yaxis_radio)

        self.figure.delaxes(self.axes)
        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8])

        if selected_radio == 1:
            pass
        else:
            pass

        self.canvas.draw()
        self.toolbar.update()
        