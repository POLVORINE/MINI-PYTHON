import tkinter as tk


# Iniciar  la aplicación/inferfaz
def botonscanner(cuadrodetexto,label):  # scanner
    # programa ejemplo
    textoprocesado = ""
    progejemplo = cuadrodetexto.get("1.0", "end-1c")
    from Pruebas.MainFalso import lexer
    lexer.input(progejemplo)  # mandamos lo que esta en el cuadro de texto para el lexer
    for token in lexer:  # por cada token que encuentre en el programa ejemplo
        textoprocesado += f"TokenTipo : {token.type}, VALOR: {token.value}\n"
    # imprime a la izquierda lo que encontro
    label.config(text=textoprocesado)


# Función que se ejecuta cuando se presiona el boton parser
def botonparser(cuadrodetexto):
    progejemplo = cuadrodetexto.get("1.0", "end-1c")
    from Pruebas.MainFalso import parser
    parser.parse(progejemplo)


def crearInterfaz(ventana):
    # DE AQUI PARA ABAJO ES GRAFICACION
    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("COM PAILER")
    # Crear tres marcos en la ventana
    marco_uno = tk.Frame(ventana)
    marco_dos = tk.Frame(ventana)
    marco_tres = tk.Frame(ventana)
    marco_cuatro = tk.Frame(ventana)
    # Configurar la geometría de los marcos
    ventana.grid_rowconfigure(0, weight=1)
    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)
    ventana.columnconfigure(2, weight=1)
    ventana.columnconfigure(3, weight=1)
    # posiciones en la interfaz
    marco_uno.grid(row=0, column=0, sticky="nsew")
    marco_dos.grid(row=0, column=1, sticky="nsew")
    marco_tres.grid(row=0, column=2, sticky="nsew")
    marco_cuatro.grid(row=0, column=3, sticky="nsew")
    # TAMAÑO Y TIPO DE FUENTE DE LA APLICACION
    font = ("Helvetica", 16)
    # COLORES DE LA INTERFAZ
    color_AzulOscuro = "#3A405A"
    color_AzulPastel = "#AEC5EB"
    color_RosaPastel = "#FFDCF4"
    color_GrisPastel = "#DEDBD2"
    color_VerdePastel = "#DFF2BF"
    color_VerdeOscuro = "#C7E9C0"
    # Agrega un cuadro de Texto en la parte izquierda
    cuadrodetexto = tk.Text(marco_uno, height=10, width=30, font=font, bg=color_GrisPastel)
    cuadrodetexto.pack(fill="both", expand=True)
    # Agrega un botón en la parte central
    boton_scanner = tk.Button(marco_dos, text="SCANNER", command=botonscanner, font=font, bg=color_RosaPastel)
    boton_scanner.pack()
    boton_parser = tk.Button(marco_dos, text="PARSER", command=botonparser, font=font, bg=color_RosaPastel)
    boton_parser.pack()
    # agrega un label a la derecha que sera donde se mostrara la salida del scanner
    label = tk.Label(marco_tres, text='', font=font, bg=color_GrisPastel)
    label.pack(fill="both", expand=True)
    # Agrega un cuadro de Texto en la parte izquierda
    label2 = tk.Label(marco_cuatro, text='joder', font=font, bg=color_AzulPastel)
    label2.pack(fill="both", expand=True)
