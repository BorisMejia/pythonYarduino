import tkinter as tk
import json
import serial
import requests

class App:
    def __init__(self, root, puerto_serial):
        self.root = root
        self.root.title("Exportador de Datos")

        # Variables para almacenar el peso y la estatura
        self.peso_var = tk.DoubleVar()
        self.estatura_var = tk.DoubleVar()

        # Configurar la comunicación serial con Arduino
        self.ser = serial.Serial(puerto_serial, 9600, timeout=1)

        # Marco principal para centrar los elementos
        marco = tk.Frame(root)
        marco.pack(padx=20, pady=20)

        # Etiqueta e input para el peso
        tk.Label(marco, text="Peso (kg):").grid(row=0, column=0, pady=5)
        tk.Entry(marco, textvariable=self.peso_var, width=20).grid(row=0, column=1, pady=5)

        # Etiqueta e input para la estatura
        tk.Label(marco, text="Estatura (cm):").grid(row=1, column=0, pady=5)
        tk.Entry(marco, textvariable=self.estatura_var, width=20).grid(row=1, column=1, pady=5)

        # Botón para exportar los datos a JSON
        tk.Button(marco, text="Exportar", command=self.exportar_json, width=15).grid(row=2, column=0, columnspan=2, pady=10)

        # Configurar la función para leer datos del puerto serial
        self.root.after(100, self.leer_datos_serial)

    def exportar_json(self):
        # Obtener los valores de peso y estatura
        peso = self.peso_var.get()
        estatura = self.estatura_var.get()

        # Crear un diccionario con los datos
        datos = {"peso": peso, "estatura": estatura}

        # Convertir el diccionario a formato JSON
        datos_json = json.dumps(datos, indent=4)

        # Enviar los datos a la aplicación web mediante una solicitud POST
        url = "url/endpoint"  # Reemplaza con la URL de tu aplicación web
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url, data=datos_json, headers=headers)

            # Verificar si la solicitud fue exitosa (código de respuesta 200)
            if response.status_code == 200:
                print("Datos exportados correctamente")
            else:
                print("Error al exportar datos. Código de respuesta:", response.status_code)

        except Exception as e:
            print("Error en la solicitud:", e)

        # Guardar el JSON en un archivo
        with open("datos.json", "w") as archivo:
            archivo.write(datos_json)

        # Puedes imprimir un mensaje para verificar en la consola
        print("Datos exportados:", datos_json)

    def leer_datos_serial(self):
        # Intentar leer datos del puerto serial
        try:
            linea = self.ser.readline().decode().strip()
            # Aquí puedes procesar la línea recibida según el formato de tus datos
            print("Datos recibidos:", linea)
        except serial.SerialException:
            print("Error al leer datos del puerto serial.")

        # Configurar la función para leer datos del puerto serial nuevamente después de un breve intervalo
        self.root.after(100, self.leer_datos_serial)

# Crear la ventana principal
root = tk.Tk()

# Configurar el tamaño de la ventana y centrarla
ancho_ventana = 400
alto_ventana = 200

# Obtener la resolución de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (ancho_pantalla / 2) - (ancho_ventana / 2)
y = (alto_pantalla / 2) - (alto_ventana / 2)

# Establecer la geometría de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{int(x)}+{int(y)}")

# Puerto serial al que está conectado Arduino (debes ajustar esto según tu configuración)
puerto_serial_arduino = 'COM3'  # Reemplaza 'COM3' con el puerto correcto

# Iniciar la aplicación con la configuración del puerto serial
app = App(root, puerto_serial_arduino)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()