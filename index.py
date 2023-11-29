import tkinter as tk
import json
import requests

class App: 
    def __init__(self, root):
        self.root = root
        self.root.title("Exportar Datos")
        
    # Variables para almacenar el peso y la estatura
        self.peso_var=tk.DoubleVar()
        self.estatura_var=tk.DoubleVar()

    # contenedor principal para los elementos
        container = tk.Frame(root)
        container.pack(padx=20, pady=20)

    # Etiqueta e input para el peso
        tk.Label(container, text="Peso: ").grid(row=0, column=0)
        tk.Entry(container, textvariable=self.peso_var).grid(row=0, column=1)
    
    # Etiqueta e input para la estatura
        tk.Label(container, text="Estatura: ").grid(row=1, column=0)
        tk.Entry(container, textvariable=self.estatura_var).grid(row=1,column=1)
    
    # Botón para exportar los datos a JSON
        tk.Button(container, text="Exportar", command=self.exportar_json).grid(row=2, column=0, columnspan=2)

    def exportar_json(self):
        # Obtener los valores de peso y estatura
        peso = self.peso_var.get()
        estatura = self.estatura_var.get()

        # Crear un diccionario con los datos
        datos = {"peso": peso, "estatura": estatura}   

        # Convertir el diccionario a formato JSON
        datos_json = json.dumps(datos, indent=4)

        # Enviar los datos a la aplicación web mediante una solicitud POST
        url = "url/endpoint"
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
        with open("datos_json","w") as archivo:
            archivo.write(datos_json) 
        # Puedes imprimir un mensaje para verificar en la consola
        print("Datos exportados", datos_json) 

# Crear la ventana principal
root =tk.Tk()

# Configurar el tamaño de la ventana y centrarla
ancho_ventana = 300
alto_ventana = 150

# Obtener la resolución de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (ancho_pantalla / 2) - (ancho_ventana / 2)
y = (alto_pantalla / 2) - (alto_ventana / 2)

# Establecer la geometría de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{int(x)}+{int(y)}")

# Iniciar la aplicación
app = App(root)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()