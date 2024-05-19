import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def incarca_variabile_env(t_env):
    if os.path.exists(t_env):
        with open(t_env, 'r') as file:
            for linie in file:
                cheie, valoare = linie.strip().split('=')
                os.environ[cheie] = valoare
    else:
        print(f"Fișierul {t_env} nu poate fi găsit.")
    #Pentru partea de logare în campus am folosit informațiile gâsite la: https://thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python
def autentificare_pe_cv():
    # Inițializare driver Selenium
    driver = webdriver.Chrome()  #Putem folosi și alte drivere (ex:Edge)

    # Navigare către pagina de login a platformei CV
    driver.get("https://cv.upt.ro/login/index.php")

    try:
        # Așteaptă până când se încarcă pagina de login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

        # Obține credențialele din variabilele de mediu
        username = os.getenv("CV_USERNAME")
        password = os.getenv("CV_PASSWORD")

        # Verifică dacă variabilele de mediu pentru username și password sunt setate și nu sunt goale
        if not username or not password:
            raise ValueError("Variabilele de mediu CV_USERNAME sau CV_PASSWORD nu sunt setate sau sunt goale")

        # Introducerea credențialelor în câmpurile de login
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)

        # Apăsarea butonului de login
        driver.find_element(By.ID, "loginbtn").click()

        # Așteaptă până când pagina de start este încărcată complet
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-my-index")))

    except Exception as e:
        print("A apărut o eroare în timpul autentificării:", e)
        driver.quit()  # Închide browser-ul în caz de eroare
        return None

    return driver

def extrage_informatii_cursuri(driver):
    try:
        # Accesează pagina cu cursurile
        driver.get("https://cv.upt.ro/my/courses.php")

        # Așteaptă până când pagina cu cursurile este încărcată complet
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "coursename")))

        # Extrage informațiile despre cursuri
        cursuri = driver.find_elements(By.CLASS_NAME, "coursename")
        print(cursuri)
        # Iterăm prin fiecare curs și salvăm informațiile despre secțiuni într-un fișier text separat
        for i in range(len(cursuri)):
            # Obținem numele cursului
            nume_curs = cursuri[i].text.split("\n")[1]
            cursuri = driver.find_elements(By.CLASS_NAME, 'coursename')
            cursuri[i].click()
            # Extragem secțiunile cursului
            sectiuni = driver.find_elements(By.CSS_SELECTOR, "section")
            # Creăm fișierul text pentru curs

            nume_fisier = f"{nume_curs}.txt"
            with open(nume_fisier, "w", encoding="utf-8") as fisier:
                # Scriem numele cursului în fișiere
                fisier.write(f"Nume curs: {nume_curs}\n\n")

                # programul trece prin fiecare secțiune a cursului(itereaza) și le scrie în fișier
                for sectiune in sectiuni:
                    nume_sectiune = sectiune.text
                    fisier.write(f"{nume_sectiune}\n")
                driver.back()


        print("Informațiile despre secțiunile cursurilor au fost salvate în fișiere text.")

    except Exception as e:
        print("A apărut o eroare în timpul extragerii informațiilor despre cursuri:", e)

def principal():
    # Incărcare variabile de mediu
    incarca_variabile_env('t.env')

    # Autentificare în platforma CV
    driver = autentificare_pe_cv()

    if driver:
        print("Autentificare reușită!")
        # Extrage informațiile despre cursuri și le salvează în fișiere text
        extrage_informatii_cursuri(driver)

        # Închide browser-ul
        driver.quit()
#Pe sistemul de operare Windows este obligatoriu sa efectuam verificarea că am pornit aplicația din fișierul curent
if __name__== "__main__":
    principal()