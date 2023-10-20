import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from serial import Serial

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Potentiostato Reader")

        self.serial_port = None
        self.arduino_connected = False
        self.running = False

        self.time_value = tk.StringVar()
        self.potential_value = tk.StringVar()
        self.status_text = tk.StringVar()
        self.status_text.set("Parado")

        self.create_main_frame()
        self.create_graph()

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

        stop_button = ttk.Button(main_frame, text="Stop", command=self.stop)
        stop_button.grid(row=2, column=0, pady=10)

    def create_graph(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, padx=10, pady=10)

        # data update here

    def toggle_start(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.arduino_connected:
            messagebox.showerror("Erro", "Arduino não está conectado")
            return
        self.connect_to_arduino("COM")
        self.start_arduino_process()
        self.running = True
        self.start_button.configure(text="Stop")
        self.status_text.set("Executando")

        self.data_thread = Thread(target=self.read_data) # tag to read arduino data and update graph
        self.data_thread.start()
        # self.data_thread.join()

    def stop(self):
        self.serial_port.write(b'stop')
        self.running = False
        self.start_button.configure(text="Start")
        self.status_text.set("Parado")

    def open_config(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuração")
        config_window.geometry("310x50")

        config_frame = ttk.Frame(config_window, padding=3)
        config_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(config_frame, text="Potencial:").grid(row=1, column=0, padx=10, pady=5)
        self.potential_entry = ttk.Entry(config_frame, textvariable=self.potential_value)
        self.potential_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(config_frame, text="volts").grid(row=1, column=2, padx=5, pady=5)

    def update_time(self, value):
        self.time_value.set(value)

    def read_data(self):
        # read ports A0 and A1 to get DDP and CONVERT TO CURRENT AND UPDATE GRAPH
        ...

    def connect_to_arduino(self, port):
        try:
            self.serial_port = Serial(port, baudrate=9600)
            self.arduino_connected = True
            messagebox.showinfo("Conectado", "Conectado ao Arduino")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao Arduino: {str(e)}")
            self.arduino_connected = False

    def start_arduino_process(self):
        try:
            self.serial_port.write(b'start')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o processo do Arduino: {str(e)}")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
