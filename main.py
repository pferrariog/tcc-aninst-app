from time import time

from tkinter import BOTH
from tkinter import messagebox
from tkinter import Tk
from tkinter import Toplevel
from tkinter import ttk
from tkinter import StringVar
from matplotlib.pyplot import subplots
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from serial import Serial


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Potentiostato Reader")

        self.serial = None
        self.serial_port = None
        self.data_list = []
        self.arduino_connected = False
        self.running = False
        self.start_time = 0

        self.time_value = StringVar()
        self.potential_value = StringVar()
        self.result_value = StringVar()
        self.status_text = StringVar()

        self.status_text.set("Parado")

        self.create_main_frame()
        self.create_graph()
        # self.calculate_result()

    def create_main_frame(self):
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.start_button = ttk.Button(main_frame, text="Start", command=self.toggle_start)
        self.start_button.grid(row=0, column=0, pady=10)

        config_button = ttk.Button(main_frame, text="Configuração", command=self.open_config)
        config_button.grid(row=1, column=0, pady=10)
        
        status_label = ttk.Label(main_frame, text="Status:")
        status_label.grid(row=3, column=0)

        self.status_display = ttk.Label(main_frame, textvariable=self.status_text)
        self.status_display.grid(row=4, column=0)

        self.result_frame = ttk.Frame(self.root)
        self.result_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ns")  # Coluna 1 para o frame de resultado
        self.result_frame.columnconfigure(0, weight=1)  # Redimensionar a coluna para ocupar todo o espaço disponível

        self.result_label = ttk.Label(self.result_frame, text="Resultado:")
        self.result_label.grid(row=1, column=0, pady=5, sticky="w")

        self.result_value_label = ttk.Label(self.result_frame, textvariable=self.result_value)
        self.result_value_label.grid(row=1, column=1, pady=5, sticky="w")

    def create_graph(self):
        self.figure, self.ax = subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, padx=10, pady=10)

    def toggle_start(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.running:
            self.connect_to_arduino(self.serial_port)
        self.start_arduino_process()
        self.running = True
        self.start_button.configure(text="Stop")
        self.status_text.set("Executando")

        # realtime update
        FuncAnimation(self.figure, self.get_data, frames=100, fargs=(self), interval=100)

    def stop(self):
        self.serial.write(b'p')
        self.running = False
        self.start_button.configure(text="Start")
        self.status_text.set("Parado")

    def open_config(self):
        config_window = Toplevel(self.root)
        config_window.title("Configuração")
        config_window.geometry("310x50")

        config_frame = ttk.Frame(config_window, padding=3)
        config_frame.pack(fill=BOTH, expand=True)

        ttk.Label(config_frame, text="Potencial:").grid(row=1, column=0, padx=10, pady=5)
        self.potential_entry = ttk.Entry(config_frame, textvariable=self.potential_value)
        self.potential_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(config_frame, text="volts").grid(row=1, column=2, padx=5, pady=5)

    def update_time(self, value):
        self.time_value.set(value)

    def get_data(self):
        self.data_list.append(self.serial.readline().decode('ascii'))
        self.ax.clear()
        self.ax.plot(self.data_list)        

    def connect_to_arduino(self):
        try:
            self.serial = Serial(self.serial_port, baudrate=9600)
            self.arduino_connected = True
            messagebox.showinfo("Conectado", "Conectado ao Arduino")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao Arduino: {str(e)}")
            self.arduino_connected = False

    def start_arduino_process(self):
        try:
            self.serial.write(b's')
            self.start_time = time()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o processo do Arduino: {str(e)}")

    def calculate_result(self):
        """Calculate the analysis final result"""
        default_current = 0.01
        total_time = time() - self.start_time
        q_carga = default_current * total_time
        mols = q_carga / (1 * 96485)  # eletrons envolved
        mass = mols * 1  # molar mass
        self.result_value.set(str(mass)[:8])


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# TODO save config values
# TODO add to configuration the MM, mols used
