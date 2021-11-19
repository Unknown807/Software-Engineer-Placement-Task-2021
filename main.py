# native imports
import tkinter as tk
from tkinter import messagebox

# third-party imports

# custom imports
from graph_canvas import GraphCanvas
from config_panel import ConfigPanel
from api_utils import checkConnectivity

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

        self.close_window()

    def pass_config_to_graph(self, *args):
        self.graph_canvas.create_new_plot(*args)

    def close_window(self):
        if not checkConnectivity():
            messagebox.showerror("Connection Error", "Please check your internet connection and try again")
            self.destroy()
        
if __name__ == "__main__":
    root = Main()
    root.mainloop()