import time
import board
import neopixel
import digitalio

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

