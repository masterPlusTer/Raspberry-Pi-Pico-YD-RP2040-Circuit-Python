import time
import board
import neopixel
import digitalio
import os
import gc
import microcontroller

def format_bytes(bytes_value):
    """Convierte bytes a kilobytes (KB) o megabytes (MB) según el tamaño."""
    if bytes_value < 1024:
        return f"{bytes_value} bytes"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.2f} KB"
    else:
        return f"{bytes_value / (1024 * 1024):.2f} MB"

def get_system_info():
    """Recopila y muestra detalles del sistema de manera legible."""
    print("=== Información del Sistema ===")

    # Información de la placa
    print(f"Placa: {getattr(board, 'board_id', 'Desconocida')}")

    # Información del sistema de archivos
    stats = os.statvfs('/')
    total_flash = stats[0] * stats[2]  # Tamaño total de memoria flash
    free_flash = stats[0] * stats[3]   # Memoria flash libre
    print(f"Capacidad total de memoria flash: {format_bytes(total_flash)} -----  el core de Circuit Python ocupa un MB que no se cuenta aqui ;)")
    print(f"Memoria flash libre: {format_bytes(free_flash)}")

    # Información del procesador
    print("\n=== Información del Procesador ===")
    print(f"Frecuencia de la CPU: {microcontroller.cpu.frequency / 1_000_000:.2f} MHz")
    print(f"Temperatura del microcontrolador: {microcontroller.cpu.temperature:.2f} °C")
    print(f"Núcleos disponibles: 1 (RP2040 tiene dos núcleos, pero MicroPython usa solo uno, si quieres usar los dos, es posible pero tiene truco)")

    # Información de la RAM
    print("\n=== Información de la RAM ===")
    gc.collect()  # Liberar memoria antes de medir
    total_ram = gc.mem_alloc() + gc.mem_free()
    free_ram = gc.mem_free()
    print(f"RAM total: {format_bytes(total_ram)}")
    print(f"RAM libre: {format_bytes(free_ram)}")

    # Pines disponibles
    print("\n=== Pines Disponibles ===")
    for attr in dir(board):
        if not attr.startswith("__"):
            print(f" - {attr}")

    # Información adicional del sistema operativo
    print("\n=== Información del Sistema Operativo ===")
    system_info = os.uname()
    print(f"Sistema: {system_info.sysname}")
    print(f"Versión: {system_info.release}")
    print(f"Información adicional: {system_info.version}")

# Llamar a la función para mostrar los detalles
get_system_info()




# Configura el NeoPixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)

# Configura el botón
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# Lista de colores
colors = [
    (255, 0, 0),  # Rojo
    (0, 255, 0),  # Verde
    (0, 0, 255),  # Azul
    (255, 255, 255),  # Blanco
    (0, 0, 0)  # Apagado
]
color_index = 0  # Índice del color actual

# Variable para detectar cambios en el estado del botón
button_pressed = False

while True:
    if not button.value:  # El botón está presionado (estado LOW)
        if not button_pressed:  # Detecta el flanco descendente
            button_pressed = True
            # Cambiar al siguiente color
            color_index = (color_index + 1) % len(colors)
            pixels[0] = colors[color_index]
    else:
        button_pressed = False  # El botón está liberado
    time.sleep(0.01)  # Pequeña espera para evitar rebotes

