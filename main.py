from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
import random
import os

# ===== CONFIGURACIÓN =====
VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Cambia por tu URL de YouTube
NUM_VIEWS = 5                  # Número de vistas a simular
MIN_VIEW_TIME = 30             # Tiempo mínimo de visualización (segundos)
MAX_VIEW_TIME = 120            # Tiempo máximo de visualización (segundos)
CHROME_PROFILE_PATH = "C:/Temp/ChromeProfile"  # Ruta para perfil de Chrome

# ===== CONFIGURACIÓN AVANZADA =====
def setup_driver():
    try:
        # Configurar opciones de Chrome
        chrome_options = Options()
        
        # Solucionar errores de SSL
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-web-security')
        
        # Configuración para evitar detección
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar perfil de usuario
        chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
        
        # Configurar agente de usuario aleatorio
        ua = UserAgent()
        user_agent = ua.random
        chrome_options.add_argument(f'user-agent={user_agent}')
        print(f"Usando User-Agent: {user_agent}")
        
        # Configurar ChromeDriver
        service = Service(executable_path='chromedriver.exe')  # Asegúrate de tenerlo en la misma carpeta
        
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error al configurar el driver: {str(e)}")
        return None

# ===== SIMULADOR DE VISTAS =====
def youtube_view_simulator():
    print("==== INICIANDO SIMULADOR DE VISTAS DE YOUTUBE ====")
    print(f"Objetivo: {NUM_VIEWS} vistas para el video")
    print(f"URL: {VIDEO_URL}")
    
    driver = setup_driver()
    if not driver:
        print("No se pudo iniciar Chrome. Verifica la instalación.")
        return

    try:
        # Configurar tamaño de ventana
        driver.set_window_size(1200, 800)
        print("Navegador iniciado correctamente")
        
        for view_count in range(1, NUM_VIEWS + 1):
            print(f"\n--- Vista #{view_count} ---")
            
            try:
                # Navegar al video
                print(f"Cargando video...")
                driver.get(VIDEO_URL)
                
                # Esperar a que cargue la página
                wait_time = random.uniform(3, 7)
                time.sleep(wait_time)
                
                # Reproducir el video si está pausado
                try:
                    play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                    button_state = play_button.get_attribute("aria-label")
                    
                    if "Play" in button_state or "Reproducir" in button_state:
                        play_button.click()
                        print("Reproducción iniciada")
                    else:
                        print("El video ya está reproduciéndose")
                except Exception as e:
                    print(f"No se pudo iniciar reproducción: {str(e)}")
                
                # Tiempo de visualización aleatorio
                view_duration = random.randint(MIN_VIEW_TIME, MAX_VIEW_TIME)
                print(f"Tiempo de visualización: {view_duration} segundos")
                
                # Simular comportamiento humano durante la reproducción
                start_time = time.time()
                while time.time() - start_time < view_duration:
                    # Scroll aleatorio
                    if random.random() > 0.7:
                        scroll_amount = random.randint(200, 600)
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        print(f"Desplazamiento: {scroll_amount}px")
                    
                    # Pausas aleatorias
                    sleep_time = random.uniform(2, 8)
                    time.sleep(sleep_time)
                
                print(f"Vista #{view_count} completada")
                
            except Exception as e:
                print(f"Error durante la vista: {str(e)}")
                print("Reiniciando navegador para la próxima vista...")
                driver.quit()
                driver = setup_driver()
                if not driver:
                    print("No se pudo reiniciar el navegador. Abortando.")
                    return
        
        print("\n==== SIMULACIÓN COMPLETADA CON ÉXITO ====")
        print(f"Total de vistas simuladas: {NUM_VIEWS}")
        
    except Exception as e:
        print(f"ERROR CRÍTICO: {str(e)}")
    finally:
        if driver:
            driver.quit()

# ===== EJECUCIÓN PRINCIPAL =====
if __name__ == "__main__":
    # Crear directorio para perfil si no existe
    if not os.path.exists(CHROME_PROFILE_PATH):
        os.makedirs(CHROME_PROFILE_PATH)
        print(f"Directorio de perfil creado: {CHROME_PROFILE_PATH}")
    
    youtube_view_simulator()
    
    # Mantener la consola abierta (solo para Windows)
    if os.name == 'nt':
        input("\nPresiona Enter para salir...")
