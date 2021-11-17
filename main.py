# native imports
import tkinter as tk

# third-party imports

# custom imports
from graph_canvas import GraphCanvas
from config_panel import ConfigPanel

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("820x580")
        self.title("Data Plotter")

        # the figure for plotting data
        self.graph_canvas = GraphCanvas(self)
        self.graph_canvas.canvas.get_tk_widget().pack(
            side="right", fill="both", expand=True,
        )

        # the configuration panel that gets the data
        self.config_panel = ConfigPanel(self)
        self.config_panel.pack(
            side="left", fill="both", expand=True, 
            padx=5
        )
        
if __name__ == "__main__":
    root = Main()
    root.mainloop()