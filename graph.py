from tkinter import Tk, TOP, BOTH
import matplotlib
from pandas import DataFrame

# tkinter integration
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


def get_input_data():
    data = {
        "volts": [1,2,3,4,5],
        "corrente": [0.2, 0.5, 0.7, 1, 1.8]
    }
    return DataFrame(data)


class App(Tk):
    """App creation class"""
    def __init__(self):
        super().__init__()
        self.title("Tk Charts")
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
        dframe = dframe[["volts", "corrente"]].groupby("volts").sum()
        dframe.plot(
            kind="line", 
            ax=axes, 
            color="b", 
            title="test data", 
            fontsize="8", 
            marker="o"
        )
