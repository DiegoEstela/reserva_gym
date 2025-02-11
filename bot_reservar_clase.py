from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def login_to_platform(driver, username, password):
    print("Abriendo la página de login...")
    driver.get("https://www.trainingymapp.com/webtouch/")

    try:
        user_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="user"]'))
        )
        pass_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="pass"]')

        user_input.send_keys(username)
        pass_input.send_keys(password + Keys.RETURN)

        WebDriverWait(driver, 3).until(EC.url_contains("dashboard"))
        print("Inicio de sesión exitoso.")
    except Exception as e:
        print(f"Error durante el login: {e}")

def navigate_to_actividades(driver):
    try:
        print("Buscando y haciendo clic en 'Actividades'...")

        actividades_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[ng-class*='indice==6'][tg-link=\"'/actividades'\"]"))
        )
        actividades_element.click()

        WebDriverWait(driver, 3).until(EC.url_contains("actividades"))
        print("Se hizo clic en 'Actividades'.")
    except Exception as e:
        print(f"Error al hacer clic en 'Actividades': {e}")

def close_modal_and_select_circuit_training(driver):
    try:
        print("Intentando cerrar modal si está presente...")

        try:
            modal_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal"))
            )
            backdrop_element = driver.find_element(By.CLASS_NAME, "modal-backdrop")
            backdrop_element.click()
            WebDriverWait(driver, 3).until(EC.invisibility_of_element(modal_element))
            print("Modal cerrado exitosamente.")
        except:
            print("No se encontró modal, continuando...")

        print("Buscando el elemento 'BODY POWER'...")
        circuit_training_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='BODY POWER']"))
        )
        circuit_training_element.click()
        print("Se hizo clic en 'BODY POWER'.")
    except Exception as e:
        print(f"Error al manejar el modal o al hacer clic en 'BODY POWER': {e}")

def click_reserve_and_complete_process(driver):
    try:
        reserve_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-tg-modal-actividad[ng-if='canPushButtonToBook']"))
        )
        reserve_button.click()
        
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "confirmation-message"))
        )
        print("Reserva realizada con éxito.")
    except Exception as e:
        print(f"Error al hacer clic en 'Reservar': {e}")

def main():
    USERNAME = "die.estela@gmail.com"
    PASSWORD = "Diee3601!"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        login_to_platform(driver, USERNAME, PASSWORD)
        navigate_to_actividades(driver)
        close_modal_and_select_circuit_training(driver)
        click_reserve_and_complete_process(driver)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        print("Cerrando navegador...")

if __name__ == "__main__":
    main()
