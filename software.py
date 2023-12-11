import tkinter as tk
from tkinter import ttk
import pandas as pd
from scapy.all import sniff, IP
import matplotlib.pyplot as plt

# Lista para almacenar los datos
data = []


# Función de callback para cada paquete capturado
def packet_callback(packet):
    if IP in packet:
        row = {
            "IP de orígen": packet[IP].src,
            "IP de destino": packet[IP].dst,
            "Protocolo": packet[IP].proto,
            "Longitud de paquete": len(packet),
            "Tiempo": packet.time,
        }
        data.append(row)


# Capturar paquetes
sniff(prn=packet_callback, store=0, count=50)

# Crear DataFrame de Pandas
df = pd.DataFrame(data)
print(df)


# Funciones para mostrar diferentes gráficas
def comunicacionesExitosas():
    # cada punto con un color diferente
    plt.scatter(df["IP de orígen"], df["IP de destino"], cmap="Blues", alpha=0.5)
    plt.title("Comunicaciones exitosas")
    plt.xlabel("IP de orígen")
    plt.ylabel("IP de destino")
    plt.show()


def frecuenciasProtocolos():
    protocol_counts = df["Protocolo"].value_counts()

    # clasificar por numero de protocolo
    case = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        50: "ESP",
        51: "AH",
        58: "ICMPv6",
        88: "EIGRP",
        89: "OSPF",
        103: "PIM",
        112: "VRRP",
        115: "L2TP",
    }

    # gráfica de pastel
    plt.pie(
        protocol_counts,
        labels=protocol_counts.index.map(case),
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
        colors=[
            "#ff9999",
            "#66b3ff",
            "#99ff99",
            "#ffcc99",
            "#ffccff",
            "#ffff99",
            "#ff6666",
            "#66ff99",
            "#ff99ff",
            "#99ffff",
            "#ff9966",
        ],
    )
    plt.title("Clasificación de protocolo")
    plt.show()

def tiempoLongitud():
    # grafica de linea
    plt.plot(df["Tiempo"], df["Longitud de paquete"], color="green")
    plt.title("Trafico a lo largo del tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Longitud de paquete")
    plt.show()
    

    
# Crear ventana principal
root = tk.Tk()
root.title("Análisis de tráfico en la red")

# tabla de todos los paquetes capturados
tree = ttk.Treeview(root)
tree["columns"] = ("IP de orígen", "IP de destino", "Protocolo", "Longitud de paquete")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("IP de orígen", anchor=tk.W, width=150)
tree.column("IP de destino", anchor=tk.W, width=150)
tree.column("Protocolo", anchor=tk.W, width=100)
tree.column("Longitud de paquete", anchor=tk.W, width=100)
tree.heading("#0", text="", anchor=tk.W)
tree.heading("IP de orígen", text="IP de orígen", anchor=tk.W)
tree.heading("IP de destino", text="IP de destino", anchor=tk.W)
tree.heading("Protocolo", text="Protocolo", anchor=tk.W)
tree.heading("Longitud de paquete", text="Longitud de paquete", anchor=tk.W)
tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

# insertar datos en la tabla
for index, row in df.iterrows():
    tree.insert(
        "",
        index,
        text="",
        values=(
            row["IP de orígen"],
            row["IP de destino"],
            row["Protocolo"],
            row["Longitud de paquete"],
        ),
    )

# Botones para mostrar gráficas
length_button = tk.Button(
    root, text="Frecuencia de protocolo", command=frecuenciasProtocolos
)
length_button.grid(row=1, column=0, sticky="ew")

ip_button = tk.Button(
    root, text="Comunicaciones exitosas", command=comunicacionesExitosas
)
ip_button.grid(row=1, column=1, sticky="ew")

trafico_tiempo_button = tk.Button(
    root, text="Trafico a lo largo del tiempo", command=tiempoLongitud
)
trafico_tiempo_button.grid(row=1, column=2, sticky="ew")

# Configure rows and columns to resize with the window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# arrancar app principal
root.mainloop()
