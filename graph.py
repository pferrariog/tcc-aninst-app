from tkinter import Tk, TOP, BOTH
from tkinter import ttk
import matplotlib
from pandas import DataFrame, read_excel

# tkinter integration
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


def get_input_data():
    data = read_excel("fake_data.xlsx")
    data.reset_index(drop=True)
    return data


class App(Tk):
    """App creation class"""
    def __init__(self):
        super().__init__()
        self.title("Tk Charts")
        self.resizable(0,0)
        # creates the chart drawing area
        self.figure = Figure((6,4), dpi=100)
        dframe = get_input_data()
        self.whole_creation(dframe)
        
    def setup_chart(self):
        # link figure to tkinter canvas
        canvas = FigureCanvasTkAgg(self.figure, self)
        # built in toolbar
        NavigationToolbar2Tk(canvas, self)
        return canvas

    def whole_creation(self, dframe):
        canvas = self.setup_chart()
        axes = self.figure.add_subplot(111)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        dframe = dframe[["potencial/v", "corrente/a"]].groupby("potencial/v").sum()
        dframe.plot(
            kind="line", 
            ax=axes, 
            color="b", 
            title="test data", 
            fontsize="8", 
        )
