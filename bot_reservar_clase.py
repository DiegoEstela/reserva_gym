from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains import ActionChains

def login_to_platform(driver, username, password):
    print("Abriendo la página de login...")
    driver.get("https://www.trainingymapp.com/webtouch/")
    time.sleep(1) 
    
    try:
        user_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="user"]')  
        pass_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="pass"]')  
        
        user_input.send_keys(username)
        pass_input.send_keys(password + Keys.RETURN)
        
        time.sleep(1)  

        print("Intento de inicio de sesión completado.")
    except Exception as e:
        print(f"Error durante el login: {e}")

def navigate_to_actividades(driver):
    try:
        print("Buscando y haciendo clic en 'Actividades'...")

        actividades_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[ng-class*='indice==6'][tg-link=\"'/actividades'\"]"))
        )

        actividades_element.click()
        print("Se hizo clic en 'Actividades'.")

        time.sleep(3) 
    except Exception as e:
        print(f"Error al hacer clic en 'Actividades': {e}")

def close_modal_and_select_circuit_training(driver):
    try:
        window_width = driver.execute_script("return window.innerWidth")
        window_height = driver.execute_script("return window.innerHeight")

        click_x = window_width // 4
        click_y = window_height // 4

        print("Intentando hacer clic fuera del centro...")
        actions = ActionChains(driver)
        actions.move_by_offset(click_x, click_y).click().perform()
        print("Clic realizado fuera del centro.")

        # Esperamos y verificamos si el modal está visible
        try:
            modal_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal"))
            )
            backdrop_element = driver.find_element(By.CLASS_NAME, "modal-backdrop")
            backdrop_element.click()
            print("Se hizo clic en el fondo del modal.")
            
            WebDriverWait(driver, 10).until(EC.invisibility_of_element(modal_element))
            print("Modal cerrado.")
        except:
            print("No se encontró modal visible, continuando.")

        print("Buscando el elemento 'BODY POWER'...")

        # Desplazamos la página hacia el final para asegurar que todo se cargue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperamos para asegurar que el scroll se aplique

        # Intentamos esperar hasta que el elemento esté visible
        circuit_training_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='BODY POWER']"))
        )

        # Aseguramos que el elemento está visible en la pantalla
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", circuit_training_element)
        time.sleep(1)  # Esperamos a que la animación termine

        # Verificamos si el elemento está disponible y clickeable
        if circuit_training_element.is_displayed() and circuit_training_element.is_enabled():
            print("Haciendo clic en 'BODY POWER'...")
            circuit_training_element.click()
            print("Se hizo clic en 'BODY POWER'.")
        else:
            print("El elemento 'BODY POWER' no es clickeable o visible.")
    except Exception as e:
        print(f"Error al manejar el modal o al hacer clic en 'BODY POWER': {e}")

def click_reserve_and_complete_process(driver):
    try:
        reserve_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-tg-modal-actividad[ng-if='canPushButtonToBook']"))
        )

        reserve_button.click()
        print("Se hizo clic en 'Reservar'.")

        time.sleep(2)

        print("¡Proceso completado con éxito! Se realizó la reserva correctamente.")
    except Exception as e:
        print(f"Error al hacer clic en 'Reservar' o completar el proceso: {e}")

def main():
    USERNAME = "die.estela@gmail.com"
    PASSWORD = "Diee3601!"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-user-data-dir")  # Evitar conflictos con el directorio de datos
    # options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin interfaz gráfica)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        login_to_platform(driver, USERNAME, PASSWORD)
        navigate_to_actividades(driver)
        close_modal_and_select_circuit_training(driver)
        click_reserve_and_complete_process(driver)
        
        input("Presiona Enter para cerrar...") 
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        print("Cerrando navegador...")

if __name__ == "__main__":
    main()
