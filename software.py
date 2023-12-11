# PARA USAR INSTALAR ESTAS LIBRERIAS
# pip install tk
# pip install pandas
# pip install scapy
# pip install matplotlib

import tkinter as tk
from tkinter import ttk
import pandas as pd
from scapy.all import sniff, IP
import matplotlib.pyplot as plt

data = []


def packet_callback(packet):
    if IP in packet:
        row = {
            "IP de orígen": packet[IP].src,
            "IP de destino": packet[IP].dst,
            "Protocolo": packet[IP].proto,
            "Longitud de paquete": len(packet),
            "Tiempo": packet.time,
        }
        data.append(row)  # agregar a la lista el paquete recibido


sniff(
    prn=packet_callback,  # llamar la funcion cada vez que se reciba un paquete
    store=0,  # no guardar los paquetes en memoria
    count=50,
)  # numero de paquetes a capturar

df = pd.DataFrame(data)  # hacerlo df
print(df)


def intercambioDePaquetes():
    plt.scatter(df["IP de orígen"], df["IP de destino"], cmap="Blues", alpha=0.5)
    plt.title("Intercambio de paquetes")
    plt.xlabel("IP de orígen")
    plt.ylabel("IP de destino")
    plt.show()


def frecuenciasProtocolos():
    protocol_counts = df["Protocolo"].value_counts()
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
    plt.plot(df["Tiempo"], df["Longitud de paquete"], color="green")
    plt.title("Trafico a lo largo del tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Longitud de paquete")
    plt.show()


root = tk.Tk()
root.title("Análisis de tráfico en la red")

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

length_button = tk.Button(
    root, text="Frecuencia de protocolo", command=frecuenciasProtocolos
)
length_button.grid(row=1, column=0, sticky="nsew", ipadx=10, ipady=10, padx=10, pady=10)

ip_button = tk.Button(
    root, text="Intercambio de paquetes", command=intercambioDePaquetes
)
ip_button.grid(row=1, column=1, sticky="nsew", ipadx=10, ipady=10, padx=10, pady=10)

trafico_tiempo_button = tk.Button(
    root, text="Trafico a lo largo del tiempo", command=tiempoLongitud
)
trafico_tiempo_button.grid(row=1, column=2, sticky="nsew", ipadx=10, ipady=10, padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
