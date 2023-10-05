import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Arduino")

        self.serial_port = None
        self.arduino_connected = False
        self.running = False

        self.time_value = tk.StringVar()
        self.potential_value = tk.StringVar()
        self.status_text = tk.StringVar()
        self.status_text.set("Parado")

        self.create_main_frame()
        self.create_graph()

        # Conectar ao Arduino (substitua 'COMX' pela porta serial correta do seu Arduino)
        self.connect_to_arduino('COMX')

    def create_main_frame(self):
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.start_button = ttk.Button(main_frame, text="Start", command=self.toggle_start)
        self.start_button.grid(row=1, column=0, pady=10, sticky="w")

        config_button = ttk.Button(main_frame, text="Configuração", command=self.open_config)
        config_button.grid(row=0, column=0, pady=10, sticky="w")

        status_label = ttk.Label(main_frame, text="Status:")
        status_label.grid(row=2, column=0, sticky="w")

        self.status_display = ttk.Label(main_frame, textvariable=self.status_text)
        self.status_display.grid(row=3, column=0, sticky="w")

        stop_button = ttk.Button(main_frame, text="Stop", command=self.stop)
        stop_button.grid(row=4, column=0, pady=10, sticky="w")


    def create_graph(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, padx=10, pady=10)

        # Inicialmente, preencha o gráfico com dados fictícios
        # self.plot_fake_data()

    def toggle_start(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.arduino_connected:
            messagebox.showerror("Erro", "Arduino não está conectado")
            return

        self.running = True
        self.start_button.configure(text="Stop")
        self.status_text.set("Executando")

        # Inicie uma thread para simular a leitura de dados do Arduino e atualizar o gráfico
        self.data_thread = threading.Thread(target=self.simulate_data)
        self.data_thread.start()

    def stop(self):
        self.running = False
        self.start_button.configure(text="Start")
        self.status_text.set("Parado")

    def open_config(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuração")
        config_window.geometry("310x100")  # Definir tamanho da janela

        # Adicionar margens de 3 pixels em todos os lados
        config_frame = ttk.Frame(config_window, padding=3)
        config_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(config_frame, text="Tempo:").grid(row=0, column=0, padx=10, pady=5)
        self.time_scale = ttk.Scale(config_frame, from_=1, to=10, orient="horizontal", command=self.update_time)
        self.time_scale.grid(row=0, column=1, padx=10, pady=5)
        self.time_scale.set(5)  # Valor padrão inicial

        ttk.Label(config_frame, text="segundos").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(config_frame, text="Potencial:").grid(row=1, column=0, padx=10, pady=5)
        self.potential_entry = ttk.Entry(config_frame, textvariable=self.potential_value)
        self.potential_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(config_frame, text="volts").grid(row=1, column=2, padx=5, pady=5)

        # Adicionar marcos de 1 a 10 à barra de progresso de tempo
        self.time_scale.set((1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)) # ???

    def update_time(self, value):
        self.time_value.set(value)

    def simulate_data(self):
        x_data = []
        y_data = []

        while self.running:
            x_data.append(len(x_data) + 1)
            y_data.append(float(self.potential_value.get()))

            if len(x_data) > 10:
                x_data.pop(0)
                y_data.pop(0)

            self.ax.clear()
            self.ax.plot(x_data, y_data)
            self.ax.set_xlabel("Tempo")
            self.ax.set_ylabel("Potencial (VOLTS)")
            self.canvas.draw()

            time.sleep(float(self.time_scale.get()))

    def connect_to_arduino(self, port):
        # try:
        #     self.serial_port = serial.Serial(port, baudrate=9600)
        #     self.arduino_connected = True
        #     messagebox.showinfo("Conectado", "Conectado ao Arduino")
        # except Exception as e:
        #     messagebox.showerror("Erro", f"Erro ao conectar ao Arduino: {str(e)}")
        #     self.arduino_connected = False
        pass

    def start_arduino_process(self):
        # if not self.arduino_connected:
        #     messagebox.showerror("Erro", "Arduino não está conectado")
        #     return

        # try:
        #     # Envie um comando para iniciar o processo do Arduino (substitua 'start' pelo comando correto)
        #     self.serial_port.write(b'start')

        #     self.running = True
        #     self.start_button.configure(text="Stop")
        #     self.status_text.set("Executando")

        #     # Inicie uma thread para simular a leitura de dados do Arduino e atualizar o gráfico
        #     self.data_thread = threading.Thread(target=self.simulate_data)
        #     self.data_thread.start()
        # except Exception as e:
        #     messagebox.showerror("Erro", f"Erro ao iniciar o processo do Arduino: {str(e)}")
        pass


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

main()