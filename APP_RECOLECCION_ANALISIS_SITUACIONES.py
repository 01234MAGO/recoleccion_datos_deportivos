# COMPLETAR !!!

fecha = 'desempate'

equipo_principal = 'SPORTING'
color_1_principal = '#0578EF'
color_2_principal = 'white'

equipo_rival = 'SAN CARLOS'
color_1_rival = 'red'
color_2_rival = 'white'

color_out = 'gray'

import tkinter as tk
import json
from datetime import datetime, timedelta

# Inicializar la lista de eventos y el tiempo del partido
eventos = []
eventos_principal = []
eventos_rival = []

tiempo_inicio = None
tiempo_pasado = timedelta()

# Funcion para alternar entre iniciar y detener el cronometro
def alternar_cronometro():
    global tiempo_inicio, tiempo_pasado
    if tiempo_inicio is None:
        tiempo_inicio = datetime.now()
        mensaje_estado.config(text="Cronometro iniciado", fg="blue")
        boton_cronometro.config(text="STOP")
        actualizar_tiempo_cronometro()
    else:
        tiempo_pasado += datetime.now() - tiempo_inicio
        tiempo_inicio = None
        mensaje_estado.config(text="Cronometro detenido", fg="red")
        boton_cronometro.config(text="INICIAR")
        
# Funcion para actualizar el tiempo del cronometro en la interfaz
def actualizar_tiempo_cronometro():
    if tiempo_inicio:
        tiempo_transcurrido = datetime.now() - tiempo_inicio + tiempo_pasado
    else:
        tiempo_transcurrido = tiempo_pasado
    minutos = int(tiempo_transcurrido.total_seconds()) // 60
    segundos = int(tiempo_transcurrido.total_seconds()) % 60
    tiempo_formateado = f"{minutos:02}:{segundos:02}"
    tiempo_cronometro.config(text=tiempo_formateado)
    ventana.after(1000, actualizar_tiempo_cronometro)  # Actualizar cada segundo

# Funcion para solicitar al usuario que seleccione un comando
def solicitar_evento_secundario(evento, equipo):
    ventana_evento_secundario = tk.Toplevel()
    ventana_evento_secundario.title(f"Seleccionar comando para {evento}")
    ventana_evento_secundario.geometry("200x340")
    ventana_evento_secundario.config(bg='#000439')

    etiqueta = tk.Label(ventana_evento_secundario, text=f"SEGUNDO EVENTO {evento}:", fg='white', bg='#000439')
    etiqueta.pack(pady=5)

    # Lista de comandos personalizables para cada botón
    comandos_personalizables = {
        "GOL": ["ELABORACION", "JUEGO DIRECTO", "PELOTA PARADA", "CENTRO", "REMATE", "PENAL"],
        "CHANCE GOL": ["ELABORACION", "JUEGO DIRECTO", "PELOTA PARADA", "CENTRO", "REMATE", "PENAL"],

        "REMATE": ["AFUERA", "AL ARCO", "BLOQUEADO" ],
        "FALTA": ["PELIGRO", "DEFENSA", "ATAQUE", "TACTICA", "PENAL"],
        "TARJETA": ["AMARILLA", "DOBLE AMARILLA", "ROJA"],
        "LIBRES": ["CORNER", "OFFSIDE"],
        "ARQUERO": ["ATAJADA", "CORTE"],
        "DEFENSA": ["DUELO AEREO GANADO","DUELO AEREO PERDIDO"],
        "ATAQUE": ["CENTRO AL AREA"],
        "PASE": ["COMPLETO", "INCOMPLETO"],
        "PASE OFENSIVO": ["COMPLETO", "INCOMPLETO"],
        "PELOTA RECUPERADA": ["ZONA BAJA", "ZONA ALTA"],
        "PELOTA PERDIDA": ["ZONA BAJA", "ZONA ALTA"]
    }

    # Obtener los comandos personalizables para el evento actual
    comandos = comandos_personalizables.get(evento, [])

    # Crear botones personalizados para cada comando
    for comando in comandos:
        boton_comando = tk.Button(ventana_evento_secundario, text=comando, command=lambda c=comando: registrar_evento(evento, equipo, c), width=24, height=2)
        boton_comando.pack(pady=5)
        boton_comando.config(bg='gray', fg='white')

    # Funcion para registrar un evento con el comando seleccionado
    def registrar_evento(evento, equipo, comando):
        tiempo_transcurrido = obtener_tiempo_transcurrido()
        tiempo_formateado = formato_tiempo(tiempo_transcurrido)
        eventos.append({"evento": evento, "tiempo": tiempo_formateado, "equipo": equipo, "evento secundario": comando})
        if equipo == "Local":
            eventos_principal.append({"evento": evento, "tiempo": tiempo_formateado, "evento secundario": comando})
        elif equipo == "Visitante":
            eventos_rival.append({"evento": evento, "tiempo": tiempo_formateado, "evento secundario": comando})
        eventos_principal.sort(key=lambda x: datetime.strptime(x['tiempo'], '%M:%S'))
        eventos_rival.sort(key=lambda x: datetime.strptime(x['tiempo'], '%M:%S'))
        actualizar_feed_eventos()
        ventana_evento_secundario.destroy()


# Funcion para dar formato al tiempo
def formato_tiempo(tiempo):
    minutos = int(tiempo.total_seconds()) // 60
    segundos = int(tiempo.total_seconds()) % 60
    return f"{minutos:02}:{segundos:02}"

# Funcion para actualizar el feed de eventos
def actualizar_feed_eventos():
    feed_eventos.delete('1.0', tk.END)
    todos_los_eventos = eventos_principal + eventos_rival
    todos_los_eventos.sort(key=lambda x: x['tiempo'], reverse=True)
    for evento in todos_los_eventos:
        equipo = "Equipo Local" if evento in eventos_principal else "Equipo Visitante"
        texto_evento = f"{equipo} - Evento: {evento['evento']}, Tiempo: {evento['tiempo']}"
        if evento['evento secundario'] is not None:
            texto_evento += f", secundario: {evento['evento secundario']}"
        feed_eventos.insert(tk.END, texto_evento + "\n")
        
# Funcion para obtener el tiempo transcurrido desde el inicio del cronometro
def obtener_tiempo_transcurrido():
    if tiempo_inicio:
        return datetime.now() - tiempo_inicio + tiempo_pasado
    else:
        return tiempo_pasado

# Funcion para guardar los eventos en un archivo JSON
def guardar_eventos():
    try:
        with open(f'fecha{fecha}_vs_{equipo_rival}.json', 'w') as f:
            json.dump(eventos, f)
        mensaje_estado.config(text="GUARDADOS", fg="green")
    except Exception as e:
        mensaje_estado.config(text=f"Error al guardar eventos: {e}", fg="red")

# Funcion para eliminar el último evento
def eliminar_ultimo_evento():
    global eventos
    if eventos:
        # Obtener el último evento eliminado
        ultimo_evento_eliminado = eventos.pop()
        mensaje_evento_eliminado = f"Evento eliminado: Equipo {ultimo_evento_eliminado['equipo']} - {ultimo_evento_eliminado['evento']}, Tiempo: {ultimo_evento_eliminado['tiempo']}"

        # Insertar el mensaje de evento eliminado en la parte superior del área de texto
        feed_eventos.config(state=tk.NORMAL)  # Permitir la edicion del área de texto
        feed_eventos.insert("1.0", mensaje_evento_eliminado + "\n", "rojo")  # Insertar el mensaje en rojo al principio del texto
        feed_eventos.tag_config("rojo", foreground="red")  # Configurar el color rojo para el texto

# Función para confirmar la edición del tiempo
def confirmar_edicion_tiempo():
    global tiempo_pasado
    try:
        # Obtener los minutos y segundos ingresados por el usuario
        minutos = int(entry_minutos.get())
        segundos = int(entry_segundos.get())
        
        # Convertir minutos y segundos a un objeto timedelta
        tiempo_nuevo = timedelta(minutes=minutos, seconds=segundos)
        
        # Actualizar el tiempo pasado con el tiempo nuevo
        tiempo_pasado = tiempo_nuevo
        
        # Actualizar el tiempo del cronómetro en la interfaz
        actualizar_tiempo_cronometro()
        
        # Cerrar la ventana de edición de tiempo
        ventana_edicion_tiempo.destroy()
    except ValueError:
        # Manejar errores si los valores ingresados no son números enteros
        mensaje_estado.config(text="Error: ingrese números enteros", fg="red")

# Función para abrir la ventana de edición de tiempo
def abrir_ventana_edicion_tiempo():
    global ventana_edicion_tiempo
    ventana_edicion_tiempo = tk.Toplevel()
    ventana_edicion_tiempo.title("Editar Tiempo")
    ventana_edicion_tiempo.geometry("200x150")
    
    # Etiqueta y campo de entrada para los minutos
    tk.Label(ventana_edicion_tiempo, text="Minutos:").pack()
    global entry_minutos
    entry_minutos = tk.Entry(ventana_edicion_tiempo)
    entry_minutos.pack()
    
    # Etiqueta y campo de entrada para los segundos
    tk.Label(ventana_edicion_tiempo, text="Segundos:").pack()
    global entry_segundos
    entry_segundos = tk.Entry(ventana_edicion_tiempo)
    entry_segundos.pack()
    
    # Botón para confirmar la edición del tiempo
    tk.Button(ventana_edicion_tiempo, text="Confirmar", command=confirmar_edicion_tiempo).pack()

# Crear la ventana de la aplicacion
ventana = tk.Tk()
ventana.title("Botonera de Eventos de Fútbol")
ventana.config(bg='#000439')
ventana.resizable(width=False, height=False)

# BOTONES LOCAL
boton_gol_principal = tk.Button(ventana, text="GOL", command=lambda: solicitar_evento_secundario("GOL", equipo_principal), width=14, height=3)
boton_gol_principal.grid(row=0, column=0, padx=5, pady=5)
boton_gol_principal.config(bg=color_1_principal, fg=color_2_principal)

boton_ch_gol_principal = tk.Button(ventana, text="CHANCE DE GOL", command=lambda: solicitar_evento_secundario("CHANCE GOL", equipo_principal), width=14, height=3)
boton_ch_gol_principal.grid(row=0, column=1, padx=5, pady=5)
boton_ch_gol_principal.config(bg=color_1_principal, fg=color_2_principal)

boton_remate_principal = tk.Button(ventana, text="REMATE", command=lambda: solicitar_evento_secundario("REMATE", equipo_principal), width=14, height=3)
boton_remate_principal.grid(row=0, column=2, padx=5, pady=5)
boton_remate_principal.config(bg=color_1_principal, fg=color_2_principal)

boton_libres_principal = tk.Button(ventana, text="LIBRES", command=lambda: solicitar_evento_secundario("LIBRES", equipo_principal), width=14, height=3)
boton_libres_principal.grid(row=1, column=0, padx=5, pady=5)
boton_libres_principal.config(bg=color_out, fg=color_2_principal)

boton_falta_principal = tk.Button(ventana, text="FALTA", command=lambda: solicitar_evento_secundario("FALTA", equipo_principal), width=14, height=3)
boton_falta_principal.grid(row=1, column=1, padx=5, pady=5)
boton_falta_principal.config(bg=color_out, fg=color_2_principal)

boton_tarjeta_principal = tk.Button(ventana, text="TARJETA", command=lambda: solicitar_evento_secundario("TARJETA", equipo_principal), width=14, height=3)
boton_tarjeta_principal.grid(row=1, column=2, padx=5, pady=5)
boton_tarjeta_principal.config(bg=color_out, fg=color_2_principal)

boton_arquero_principal = tk.Button(ventana, text="ARQUERO", command=lambda: solicitar_evento_secundario("ARQUERO", equipo_principal), width=14, height=3)
boton_arquero_principal.grid(row=2, column=0, padx=5, pady=5)
boton_arquero_principal.config(bg=color_out, fg=color_2_principal)

boton_posecion_principal = tk.Button(ventana, text="DEFENSA", command=lambda: solicitar_evento_secundario("DEFENSA", equipo_principal), width=14, height=3)
boton_posecion_principal.grid(row=2, column=1, padx=5, pady=5)
boton_posecion_principal.config(bg=color_out, fg=color_2_principal)

boton_centro_principal = tk.Button(ventana, text="ATAQUE", command=lambda: solicitar_evento_secundario("ATAQUE", equipo_principal), width=14, height=3)
boton_centro_principal.grid(row=2, column=2, padx=5, pady=5)
boton_centro_principal.config(bg=color_out, fg=color_2_principal)

boton_pase = tk.Button(ventana, text="PASE", command=lambda: solicitar_evento_secundario("PASE", equipo_principal), width=14, height=1)
boton_pase.grid(row=3, column=0, padx=5, pady=5, sticky="n")
boton_pase.config(bg=color_out, fg=color_2_principal)

boton_pase_ofensivo = tk.Button(ventana, text="OFENSIVO", command=lambda: solicitar_evento_secundario("PASE OFENSIVO", equipo_principal), width=14, height=1)
boton_pase_ofensivo.grid(row=3, column=0, padx=5, pady=5, sticky="s")
boton_pase_ofensivo.config(bg=color_1_principal, fg=color_2_principal)

boton_pelota_recuperada = tk.Button(ventana, text="RECUPRDA", command=lambda: solicitar_evento_secundario("PELOTA RECUPERADA", equipo_principal), width=14, height=1)
boton_pelota_recuperada.grid(row=3, column=1, padx=5, pady=5, sticky="n")
boton_pelota_recuperada.config(bg=color_1_principal, fg=color_2_principal)

boton_pelota_perdida = tk.Button(ventana, text="PERDIDA", command=lambda: solicitar_evento_secundario("PELOTA PERDIDA", equipo_principal), width=14, height=1)
boton_pelota_perdida.grid(row=3, column=1, padx=5, pady=5, sticky="s")
boton_pelota_perdida.config(bg=color_1_principal, fg=color_2_principal)

# BOTONES VISITANTE

boton_gol_rival = tk.Button(ventana, text="GOL", command=lambda: solicitar_evento_secundario("GOL", equipo_rival), width=14, height=3)
boton_gol_rival.grid(row=0, column=3, padx=5, pady=5)
boton_gol_rival.config(bg=color_1_rival, fg=color_2_rival)

boton_ch_gol_rival = tk.Button(ventana, text="CHANCE DE GOL", command=lambda: solicitar_evento_secundario("CHANCE GOL", equipo_rival), width=14, height=3)
boton_ch_gol_rival.grid(row=0, column=4, padx=5, pady=5)
boton_ch_gol_rival.config(bg=color_1_rival, fg=color_2_rival)

boton_remate_rival = tk.Button(ventana, text="REMATE", command=lambda: solicitar_evento_secundario("REMATE", equipo_rival), width=14, height=3)
boton_remate_rival.grid(row=0, column=5, padx=5, pady=5)
boton_remate_rival.config(bg=color_out, fg=color_2_rival)

boton_libres_rival = tk.Button(ventana, text="LIBRES", command=lambda: solicitar_evento_secundario("LIBRES", equipo_rival), width=14, height=3)
boton_libres_rival.grid(row=1, column=3, padx=5, pady=5)
boton_libres_rival.config(bg=color_out, fg=color_2_rival)

boton_falta_rival = tk.Button(ventana, text="FALTA", command=lambda: solicitar_evento_secundario("FALTA", equipo_rival), width=14, height=3)
boton_falta_rival.grid(row=1, column=4, padx=4, pady=5)
boton_falta_rival.config(bg=color_out, fg=color_2_rival)

boton_tarjeta_rival = tk.Button(ventana, text="TARJETA", command=lambda: solicitar_evento_secundario("TARJETA", equipo_rival), width=14, height=3)
boton_tarjeta_rival.grid(row=1, column=5, padx=5, pady=5)
boton_tarjeta_rival.config(bg=color_out, fg=color_2_rival)

# Crear boton para iniciar/detener cronometro
boton_cronometro = tk.Button(ventana, text="INICIAR", command=alternar_cronometro, width=14, height=1)
boton_cronometro.grid(row=2, column=3, pady=4, sticky="s")
boton_cronometro.config(bg='#00BF63')

# Etiqueta para mostrar el tiempo del cronometro
tiempo_cronometro = tk.Label(ventana, text="00:00", font=("Helvetica", 20),width=14, height=2 )
tiempo_cronometro.grid(row=2, column=4, columnspan=2, pady=5)

# Crear un área de texto para mostrar los eventos registrados
feed_eventos = tk.Text(ventana, height=4, width=40)
feed_eventos.grid(row=4, column=0, columnspan=8, pady=10)

# Crear boton para eliminar el último evento sin guardar
boton_eliminar_ultimo = tk.Button(ventana, text="ELIMINAR", command=eliminar_ultimo_evento, width=14, height=2 )
boton_eliminar_ultimo.grid(row=5, column=0, columnspan=1, pady=5)
boton_eliminar_ultimo.config(bg='red')

# Crear boton para guardar eventos
boton_guardar = tk.Button(ventana, text="GUARDAR", command=guardar_eventos, width=14, height=2 )
boton_guardar.grid(row=5, column=5, columnspan=1, pady=5)
boton_guardar.config(bg='#00BF63')

# Etiqueta para mostrar el estado de la operacion de guardado
mensaje_estado = tk.Label(ventana, text="", fg="black", width=20, height=2 )
mensaje_estado.grid(row=5, column=1, columnspan=4, pady=5)

# Crear botón para abrir la ventana de edición de tiempo
boton_editar_tiempo = tk.Button(ventana, text="EDITAR", command=abrir_ventana_edicion_tiempo, width=14, height=1)
boton_editar_tiempo.grid(row=2, column=3, pady=5, sticky="n")
boton_editar_tiempo.config(bg= 'orange')

# Iniciar la aplicacion
ventana.mainloop()
