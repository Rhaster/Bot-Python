from selenium import webdriver
import time  
from datetime import datetime, timedelta
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException,TimeoutException, UnexpectedAlertPresentException , StaleElementReferenceException , ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import holidays
import re
import os
import sys
from selenium.webdriver import Firefox, FirefoxOptions

############################## BOT BILLKOM V1.0 ########################################

############################## BOT BILLKOM V1.0 ########################################
""" # Debugowanie
output_file = "xaxa.txt"
NR_Bota= 5
A = "Olsztyn Zachodni"
B = "Warszawa Centralna"
internal_error=0
oczekiwanie_web_drivera= 8 # w sekundach
""" 
## Argumenty podawane z poziomu cmd
output_file = sys.argv[1]# "xd.txt"
NR_Bota= sys.argv[2]
A = sys.argv[3]
B = sys.argv[4]
internal_error=sys.argv[5]
oczekiwanie_web_drivera= 8 # w sekundach
#Przewoznik = sys.argv[7]
###################
pl_holidays = holidays.PL(years=[2023])
dzisiaj = datetime.now()
global Logi
Logi = []

# Sprawdzamy, czy dzisiaj jest dniem roboczym
def GetNextDay(dzisiaj,pl_holidays):
    i = 1
    while True:
        date = (dzisiaj + timedelta(days=i)).weekday()
        if date <= 4 and (dzisiaj + timedelta(days=i)) not in pl_holidays:
            break
        i += 1
    return (dzisiaj + timedelta(days=i)).strftime('%d/%m/%y')
date = GetNextDay(dzisiaj,pl_holidays)
times = "10:30" 
imie = "Jan"
nazwisko = "Kowalski"
email = "jan.kowalski@example.com"
### kontener#
tabela_nazw=["Strona glowna","Wynik wyszukiwania","Wybor pociagu","Wybor miejsca","Podsumowanie","Zamowienie","Platnosc"]
##### Konfiguracja webdrivera oraz ustawienie liczników czasu
options = FirefoxOptions()
options.add_argument("--headless")
options.set_capability("moz:firefoxOptions", {"args": ["-headless"]})
def retry():
    global tabelaczasow
    tabelaczasow = []
    global blad
    blad=""
    global StartBota
    StartBota=time.time()
retry()
def bilkom(A,B,imie,nazwisko,email,tabelaczasow,times,date):
    print("Start Bota nr ",NR_Bota)
    global blad
    # Strona Pierwsza Wyszukanie Okien do wpisania
    # inicjalizacja webdrivera
    try:
        Logi.append(f"Bot bilkom nr {NR_Bota} Start")
        try:
            Logi.append(" Inicjacja przegladarki firefox")
            #driver = webdriver.Firefox()
            driver = webdriver.Firefox(options=options) ### to usunac gdy chcemy zobaczyc przegladarke (options=options)  => ()
            driver.set_window_position(0, 0)
            start_time = time.time()
            # inicjalizacja waitera 
            wait = WebDriverWait(driver,oczekiwanie_web_drivera)
        except :
            blad = "Nie udało się załadować webdrivera"
            return False
        # Strona Pierwsza Wyszukanie Okien do wpisania
        try:
            Logi.append(" Inicjacja strony billkom.pl")
            driver.get('https://bilkom.pl/')
            #driver.minimize_window()
        except Exception as e:
            Logi.append(" nie udało sie załadowac bilkom.pl")
            blad = " nie udało sie załadowac bilkom.pl"
            driver.close()
            return False
        try:
            Logi.append(" Zamykanie reklamy ")
            wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='modal-body']//img[@class='img-responsive']")))
            driver.find_element(By.XPATH,"//div[@class='modal-body']//button[@class='close']").click()
            wait.until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='modal-body']//img[@class='img-responsive']")))
        except TimeoutException:
            Logi.append(" Nie udało się załadowac strony głównej ")
            blad = " Nie udalo sie załadować strony głównej " 
            driver.close()
            return False
        except NoSuchElementException:
            Logi.append(" Nie udało się zamknac reklamy")
            blad = " Nie udalo sie zamknac reklamy na stronie głównej "
            driver.close()
            return False
        # Strona pierwsza wypełnienie formularza
        try:
            # Pierwsze pole 
            #time.sleep(1) # czas na załadowanie się listy
            Logi.append(" Ładowanie elementów strony głównej ")
            time.sleep(1) # czas na załadowanie się listy
            begging_station = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='fromStation']")))
            begging_station.click()
            begging_station.clear()
            begging_station.send_keys(A)
            time.sleep(1)  # czas na załadowanie się listy
            begging_station.send_keys(Keys.ARROW_DOWN)
            begging_station.send_keys(Keys.ENTER)
            Logi.append(" Udało się załadować element stacji poczatkowej")
            # Drugie pole
            end_station = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='toStation']")))
            end_station.click()
            end_station.clear()
            end_station.send_keys(B)
            time.sleep(1)  # czas na załadowanie się listy
            end_station.send_keys(Keys.ARROW_DOWN)
            end_station.send_keys(Keys.ENTER)
            Logi.append(" Udalo sie zaladować element stacji koncowej")
            date_element = driver.find_element(By.XPATH,("//*[@id='date']"))
            # data
            time.sleep(1)
            driver.execute_script("arguments[0].removeAttribute('readonly',0);", date_element)
            time.sleep(1)  # czas na załadowanie się listy
            date_element.click()
            date_element.clear()
            date_element.send_keys(date)
            
            time.sleep(1)  # czas na załadowanie się listy
            date_element.send_keys(Keys.ENTER)
            Logi.append(" Udalo sie zaladować element DATA")
            #czas
            time_element = driver.find_element(By.XPATH,("//*[@id='time']"))
            driver.execute_script("arguments[0].removeAttribute('readonly',0);", time_element)
            time_element.click()
            time_element.clear()
            time_element.send_keys(times)
            time_element.send_keys(Keys.ENTER)
            Logi.append(" Udalo sie zaladować element Time")
        except   StaleElementReferenceException:
            Logi.append(" Nie udało się wpisać danych do formularza Strona głowna: strona zle zaladowana  ")
            blad = "Nie udało się wpisać danych do formularza Strony glownej"
            driver.close()
            return False
        except TimeoutException:
            Logi.append(" nie udało się załadowac Strony glownej: Przekroczono limit czasu")
            blad = "nie udało się załadowac Strony glownej "
            driver.close()
            return False
        #klikniecie przycisku wyszukaj
        try:
            time.sleep(4)
            start_time = time.time()
            Logi.append(" Klikniecie przycisku wyszukaj polaczenia ")
            driver.find_element(By.XPATH,("//*[@id='search-btn']")).click()
            time.sleep(5)
        except NoSuchElementException:
            Logi.append(" Nie udalo sie kliknac przycisku wyszukaj polaczenia Strona Glowna ")
            blad = "Nie udało się kliknąć przycisku wyszukaj Strona glowna"
            driver.close()
            return False
        # Strona druga
        try:
            Logi.append(" Wyszukanie polaczenia dostepnego z przesiadkami lub bez ")
            tabelaczasow.append(time.time() - start_time)
            ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul#trips.col-xs-12.list")
            # Wyświetlenie liczby znalezionych elementów
            #print("Liczba znalezionych elementów: ", len(ul_elements))
            przycisk = 1 
            # Wyszukanie przycisków i kliknięcie ich
            for ul in ul_elements:
                try:
                    przycisk = ul.find_element(By.XPATH, "//button[@class='btn submit-btn' and @type='submit' and @onclick='checkDisabled(event, this);']")
                    wait.until(EC.element_to_be_clickable(przycisk))
                except:
                    pass
                break
            start_time1=    time.time()
            if(przycisk == 1):
                #print("nie znaleziono dostepnych polaczen Strona druga")
                Logi.append(" Nie udalo sie znalezc przycisku dostepnych polaczen Strona druga ")
                blad = "Nie udalo sie znalezc przycisku dostepnych polaczen Strona druga "
                driver.close()
                return False
            try:
                Logi.append(" sprawdzam czy poprawnie zaladowalo przycisk i czy jest dostepny ")
                przycisk.click()
            except TimeoutException:
                Logi.append(" nie udalo sie zaladowac strony 2 ")
                blad = "Nie udało się załadować  Strony 2"
                driver.close()
                return False
            try:
                Logi.append(" sprawdzam czy strona nie wykryla zbyt wielu polaczen  ")
                #driver.save_screenshot("screenshot1.png")
                przycisk = driver.find_element(By.ID,"new-order")
                time.sleep(5)
                driver.execute_script("arguments[0].scrollIntoView(true);", przycisk)  
                #driver.save_screenshot("screenshot.png")
                # Sprawdzenie, czy przycisk jest klikalny
                if przycisk.is_enabled():
                    Logi.append(" strona wykryla klikam przycisk dalej  ")
                    # Kliknięcie przycisku
                    przycisk.click()
            except NoSuchElementException:
                Logi.append(" strona nie wykryla zbyt wielu polaczen przechodze dalej  ")
                pass ## tu byla zmiana
        except TimeoutException:
            Logi.append(" nie udało sie znalezc polaczen lub strona sie nie zaladowala ")
            blad = "Nie udało się załadować  Strony 2"
            driver.close()
            return False
        try:
            time.sleep(2)
            Logi.append(" sprawdzam czy jest popup o zmianie trasy ")
            popup = wait.until(EC.visibility_of_element_located((By.ID, "stationChangedMsg")))
            zatwierdz_button = popup.find_element(By.XPATH, ".//button[contains(text(), 'Zatwierdź')]")
            if zatwierdz_button.is_displayed():
                zatwierdz_button.click()
            Logi.append("Kliknięto przycisk Zatwierdź. w popupie ")
            #print("Kliknięto przycisk Zatwierdź. w popupie ")
            time.sleep(1) # czekanie na znikniecie popupa
        except:
            Logi.append("Nie znaleziono okna z ostrzeżeniem.")
            pass
        try:
            Logi.append(" sprawdzam czy jestem na nastepnej stronie 3  ")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,("#cart"))))
            tabelaczasow.append(time.time() - start_time1)
            strona3Time=time.time()
            Logi.append("  jestem na stronie 3   ")
            Logi.append(" sprawdzam czy jest przycisk dalej i klikam go ")
            driver.find_element(By.XPATH,("//*[@id='go-to-summary']")).click()
        except  NoSuchElementException:
            blad = "Nie udało się znalezc przycisku dalej Strona 3"
            driver.close()
            return False
        except TimeoutException:
            blad = "Nie udało się załadować  Strony 3"
            driver.close()
            return False
        try:
            Logi.append(" sprawdzam czy sa elementy do wypelnienia na stronie 4")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,("#mainPassenger"))))
            Logi.append(" wykrylem pierwsze pole przechodze do pobierania ich")
            imie_Strona_3 = driver.find_element(By.XPATH,("//*[@id='passenger[0].name']"))
            pasazer_Strona_3 = driver.find_element(By.XPATH,("//*[@id='passenger[0].surname']"))
            email_Strona_3 = driver.find_element(By.XPATH,("//*[@id='passenger[0].email']"))
            email_powt_Strona_3 = driver.find_element(By.XPATH,("//*[@id='passenger[0].email2']"))
            Logi.append(" wykryto wszystkie formularze strony 4 przechodze dalej ")
        except TimeoutException:
            Logi.append(" Nie udało się załadować formularza Strona 4 ")
            blad = "Nie udało się załadować formularza Strona 4"
            driver.close()
            return False
        except NoSuchElementException:
            Logi.append(" Nie udało się znalezc elementu Strona 4")
            blad = "Nie udało się znalezc elementu Strona 4"
            driver.close()
            return False
        except:
            Logi.append(" Nie udało się załadować formularza Strona 4  ")
            blad = "Nie udało się załadować formularza Strona 4"
            driver.close()
            return False
        try:
            Logi.append(" znalazlem wszystkie formularzy strony 4 przechodze do ich wypeniania")
            imie_Strona_3.click()
            imie_Strona_3.clear()
            imie_Strona_3.send_keys(imie)
            pasazer_Strona_3.click()
            pasazer_Strona_3.clear()
            pasazer_Strona_3.send_keys(nazwisko)
            email_Strona_3.click()
            email_Strona_3.clear()
            email_Strona_3.send_keys(email)
            email_powt_Strona_3.click()
            email_powt_Strona_3.clear()
            email_powt_Strona_3.send_keys(email)
            Logi.append(" udalo sie wypelnic elementy formularza strony 4 ")
        except ElementClickInterceptedException:
            Logi.append("Nie udało się wpisać danych do formularza Strona 4")
            blad = "Nie udało się wpisać danych do formularza Strona 4"
            driver.close()
            return False
        try:
            start_time2=time.time()
            Logi.append("Szukam przycisku dalej na stronie 4 ")
            driver.find_element(By.XPATH,("//*[@id='go-to-summary']")).click();
        except NoSuchElementException:
            Logi.append("Nie udało się kliknąć przycisku  dalej Strona 4 ")
            blad = "Nie udało się kliknąć przycisku wyszukaj Strona 4"
            driver.close()
            return False
        try:
            Logi.append("czekam na zaladowanie strony 5  ")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,("#summary-wrapper"))))
            Logi.append("udalo sie zaladowac strone 5  ")
            tabelaczasow.append(time.time() - strona3Time)
            Logi.append("szukam elementuw na stronie 5 do klikniecia")
            regula_1 = driver.find_element(By.XPATH,("//*[@id='regulations']"))
            regula_2 = driver.find_element(By.XPATH,("//*[@id='carriers']"))
            platnosc = driver.find_element(By.XPATH,("//*[@id='payment']"))
            Logi.append("znalazlem elementy do klikniecia strona 5 ")
        except TimeoutException:
            Logi.append("Nie udało się załadować formularza Strona 5 : timeoutexception")
            blad = "Nie udało się załadować formularza Strona 5"
            driver.close()
            return False
        except NoSuchElementException:
            Logi.append("Nie udało się znalezc elementu na stronie 5: nosuchelementexception")
            blad = "Nie udało się znalezc elementu na stronie 5"
            driver.close()
            return False
        try:
            Logi.append("klikam w zaladowane elementy strony 5 ")
            driver.execute_script("arguments[0].scrollIntoView(true);", regula_1)
            driver.execute_script("arguments[0].click()", regula_1)
            driver.execute_script("arguments[0].scrollIntoView(true);", regula_2)
            driver.execute_script("arguments[0].click()", regula_2)
            start_time3=time.time()
            Logi.append("przechodze dalej klikajac przycisk platnosc ")
            driver.execute_script("arguments[0].scrollIntoView(true);", platnosc)
            driver.execute_script("arguments[0].click()", platnosc)
            Logi.append("Czekam na zaladowanie strony 6 ")
        except WebDriverException as e:
            Logi.append("Podczas wypełniania strony 4 nastąpił błąd")
            blad = ("Podczas wypełniania strony 4 nastąpił błąd", e)
            driver.close()
            return False
        try: 
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            current_url = driver.current_url
            Logi.append("zaladowano strone 6 sprawdzam czy poprawnie jest wyswietlony link")
            if current_url == "https://bilkom.pl/koszyk/podsumowanie":
                Logi.append(f"Bot nr {NR_Bota} ukonczyl zadanie")
                tabelaczasow.append(time.time() - start_time3)
                driver.close()
                print(f"Bot Bilkom nr {NR_Bota} pomyslnie zlozył zamówienie na Bilkom.pl")
                return True
            else:
                Logi.append("bot nie dotarl do menu platnosci")
                blad="bot nie dotarl do menu platnosci"
                driver.close()
                return False
        except WebDriverException as e:
            blad = ("Podczas przechodzenia do  5 Strony  nastąpił błąd", e)
            driver.close()
            return False
    except Exception as e :
        Logi.append("Bot napotkał nieobslugiwany blad " + str(e))
        blad = ("Bot napotkał nieobslugiwany blad "+ str(e))
        try:
            if(len(driver.window_handles)>0):
                driver.close()
            return False
        except:
            pass
        return False
    finally:
        fileu=f"Logi_Bot\\Log_bilkom_{NR_Bota}.txt"
        with open(fileu, "w") as file:
                for x in Logi:
                    file.write(str(x) + "\n")
def ender(): ## funkcja zamykajaca program z bledem
    print(f"Bot Bilkom nr :{NR_Bota} napotkal blad " + str(blad) + "  \n")
## Mechanizm ponownego podejscia po bledzie  
a=0
if(a==internal_error):
    x=bilkom(A,B,imie,nazwisko,email,tabelaczasow,times,date)
    a+=1
while a <= int(internal_error):
    Logi.append(f"Bot nr {NR_Bota} wykonuje ponowne podejscie do strony nr {a} ")
    print("Bot Billkom nr {NR_Bota} wykonuje ponowne podejscie do strony nr {a} ")
    retry()
    x=bilkom(A,B,imie,nazwisko,email,tabelaczasow,times,date)
    if(x == True):
        break
    else:
        a+=1
        tabelaczasow = []
if(x==True):
    tabelaczasow.append(time.time() - StartBota)
    #for t in tabelaczasow:
        #print(t)
    with open(output_file, "w") as file:
            for x in tabelaczasow:
                file.write(str(x) + "\n")
else:
    ender()
fileu=f"Logi_Bot\\Log_bilkom_{NR_Bota}.txt"
with open(fileu, "w") as file:
        for x in Logi:
            file.write(str(x) + "\n")
sys.exit()