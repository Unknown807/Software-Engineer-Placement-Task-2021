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

        self.plot1 = self.figure.add_subplot(111)

        self.plot1.plot([i**2 for i in range(101)])

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