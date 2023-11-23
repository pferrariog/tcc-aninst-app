from csv import DictWriter
from datetime import datetime
from os import makedirs
from time import sleep
from time import time
from tkinter import BOTH
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import ttk

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from serial import Serial
from serial.tools import list_ports


class App:
    """Potentiostat tkinter screen"""

    def __init__(self, root: Tk) -> None:
        """Variables and default methods initializer"""
        self.root = root
        self.root.title("Potentiostato Reader")

        self.serial = None
        self.arduino_connected = False
        self.running = False
        self.start_time = 0
        self.data_list: list[tuple] = []

        self.time_value = StringVar()
        self.potential_value = StringVar()
        self.result_value = StringVar()
        self.status_text = StringVar()
        self.status_text.set("Parado")

        self.create_main_frame()
        self.create_graph()

    def create_main_frame(self) -> None:
        """Create app's layout"""
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Main layout
        self.start_button = ttk.Button(main_frame, text="Start", command=self.toggle_start)
        self.start_button.grid(row=0, column=0, pady=10)
        config_button = ttk.Button(main_frame, text="Configuração", command=self.open_config)
        config_button.grid(row=1, column=0, pady=10)

        # Status
        status_label = ttk.Label(main_frame, text="Status:")
        status_label.grid(row=3, column=0)
        status_display = ttk.Label(main_frame, textvariable=self.status_text)
        status_display.grid(row=4, column=0)

        # Result
        result_frame = ttk.Frame(self.root)
        result_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        result_label = ttk.Label(result_frame, text="Resultado:")
        result_label.grid(row=1, column=0, pady=5, sticky="w")
        result_value_label = ttk.Label(result_frame, textvariable=self.result_value)
        result_value_label.grid(row=1, column=1, pady=5, sticky="w")

    def create_graph(self) -> None:
        """Create graph placeholder"""
        self.figure, self.ax = subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, padx=10, pady=10)

    def toggle_start(self) -> None:
        """Start/stop button trigger"""
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self) -> None:
        """Start the realtime animation graph"""
        if self.running:
            messagebox.showwarning("Aviso", "Processo já está em execução!")
            return
        try:
            self.connect_to_arduino()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao Arduino: {str(e)}")
            return
        messagebox.showinfo("Conectado", "Conectado ao Arduino")
        self.start_arduino_process()
        self.running = True
        self.start_button.configure(text="Stop")
        self.status_text.set("Executando")

        # realtime update
        self.animation = FuncAnimation(self.figure, self.get_data, frames=100, fargs=(self), interval=100)

    def stop(self) -> None:
        """Stop the process by sending a byte char"""
        self.serial.write(b"p")
        self.running = False
        self.start_button.configure(text="Start")
        self.status_text.set("Parado")
        # self.animation.event_source.stop()
        # self.print_output_file()
        # self.calculate_result()

    def open_config(self) -> None:
        """Create configuration screen"""
        config_window = Toplevel(self.root)
        config_window.title("Configuração")
        config_window.geometry("310x100")

        potential_frame = ttk.Frame(config_window, padding=3)
        potential_frame.pack(fill=BOTH, expand=True)

        ttk.Label(potential_frame, text="Potencial:").grid(row=1, column=0, padx=10, pady=5)
        self.potential_entry = ttk.Entry(potential_frame, textvariable=self.potential_value)
        self.potential_entry.grid(row=1, column=1, padx=10, pady=5)

    def get_data(self) -> None:
        """Plot realtime data sended by arduino"""
        current_value = self.serial.readline().decode("ascii")
        current_time = time() - self.start_time
        if "end" in current_value:
            self.stop()
            return
        self.data_list.append((current_value, current_time))
        self.ax.clear()
        self.ax.plot(zip(*self.data_list))
        self.ax.set_title("Amperograma")
        self.ax.set_ylabel("Corrente (mA)")
        self.ax.set_xlabel("Tempo (s)")

    def connect_to_arduino(self) -> None:
        """Connect to the arduino"""
        self.serial = Serial(self.get_arduino_port(), baudrate=9600, timeout=1)
        sleep(2)
        self.arduino_connected = True

    def start_arduino_process(self) -> None:
        """Start the reading process by sending a byte char"""
        try:
            self.serial.write(b"s")
            self.start_time = time()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o processo do Arduino: {str(e)}")

    # def calculate_result(self) -> None:
    #     """Calculate the analysis final result"""
    #     total_time = time() - self.start_time
    #     q_carga = ... * total_time
    #     mols = q_carga / (2 * 96485)  # eletrons envolved
    #     mass = mols * 176.12  # molar mass
    #     self.result_value.set(str(mass)[:8])

    def get_arduino_port(self) -> str | None:
        """Get connected arduino's COM port"""
        arduino_port = [str(port) for port in list_ports.comports() if "CH340" in str(port)]
        if arduino_port:
            # pattern -> com3 - arduino uno -> com3
            return arduino_port[0].split(" ")[0]
        else:
            messagebox.showerror("Não foi possível conectar com o arduino - Porta não encontrada.")

    def print_output_file(self) -> None:
        """Print the process data into a csv file"""
        makedirs("output")
        with open(f'output/data_file{datetime.now().strftime("%Y%m%d%H%M%s")}', "w+") as file:
            writer = DictWriter(file)
            writer.writeheader()
            for current, measured_time in self.data_list:
                writer.writerow({"current": current, "time": measured_time})


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
