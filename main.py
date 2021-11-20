# native imports
import tkinter as tk
from tkinter import messagebox

# third-party imports

# custom imports
from graph_canvas import GraphCanvas
from config_panel import ConfigPanel
from api_utils import checkConnectivity

class Main(tk.Tk):
    '''
    Creates the tkinter window and places the configuration panel on the left and the matplotlib canvas on the right
    and facilitates data to be passed from one to the other
    '''
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
        '''
        Passes all data of selected application/resource to the GraphCanvas object (self.graph_canvas),
        in order to plot it on the screen
        '''
        self.graph_canvas.create_new_plot(*args)

    def close_window(self):
        '''
        If there is no internet connection, then calls for data from the API cannot be made, so the program
        gives an error popup and exits
        '''
        if not checkConnectivity():
            messagebox.showerror("Connection Error", "Please check your internet connection and try again")
            self.destroy()
        
if __name__ == "__main__":
    root = Main()
    root.mainloop()