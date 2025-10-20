# prompt.py
# Samuel Angarita
# English: Prompt generation module for creating AI video animation instructions from transition types
# Español: Módulo de generación de prompts para crear instrucciones de animación de video IA desde tipos de transición

def get_prompt(transition:str)-> str:
    # Generate detailed animation prompts for AI video generation
    # Generar prompts detallados de animación para generación de video IA

    if transition == "zoom_in":
        # Create zoom-in animation prompt with specific technical parameters
        # Crear prompt de animación de zoom-in con parámetros técnicos específicos
        return "Animate this still image with a smooth camera zoom-in from 100% to 130% over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    elif transition == "zoom_out":
        # Create zoom-out animation prompt with specific technical parameters
        # Crear prompt de animación de zoom-out con parámetros técnicos específicos
        return "Animate this still image with a smooth camera zoom-out from 120% to 100% over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    elif transition == "pan":
        # Create panning animation prompt with specific technical parameters
        # Crear prompt de animación de paneo con parámetros técnicos específicos
        return "Animate this still image with a smooth left-to-right pan moving ~12% of the frame width over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    else:
        # Terminates the program with a non-zero exit code and prints the message
        # Termina el programa con código de salida distinto de cero e imprime el mensaje
        raise SystemExit(f"Error: unknown command '{transition}'. Allowed: zoom_in, zoom_out, pan")
    

# -------- tiny demo main ------------------------------------------------------
def main():
    # Demo function to test prompt generation
    # Función demo para probar generación de prompts
    
    print(get_prompt("zoom_in"))


if __name__ == "__main__":
    main()

    


    