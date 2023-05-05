from selenium import webdriver
import time  
from selenium.webdriver.support.select import Select
from datetime import datetime, timedelta
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException, UnexpectedAlertPresentException, ElementNotInteractableException
import holidays
import re
import sys
from selenium.webdriver import Firefox, FirefoxOptions


################### Bot Intercity ############################

################### Bot Intercity ############################
output_file = sys.argv[1]
NR_BOTA= sys.argv[2]
internal_error = sys.argv[3]
## DEBUG BOTA
#output_file = "TEST-INTERCITY"
#NR_BOTA = "1"
#output_file="time.txt"
#pid = os.getpid()
#output_file = output_file + "_" + str(pid) + ".txt"
###
### Opcje WebDrviera
options = FirefoxOptions()
options.add_argument("--headless")
options.set_capability("moz:firefoxOptions", {"args": ["-headless"]})
### Opcje WebDrviera
pl_holidays = holidays.PL(years=[2023])
dzisiaj = datetime.now()
# Sprawdzamy, czy dzisiaj jest dniem roboczym
def GetNextDay(dzisiaj,pl_holidays):
    i = 1
    while True:
        date = (dzisiaj + timedelta(days=i)).weekday()
        if date <= 4 and (dzisiaj + timedelta(days=i)) not in pl_holidays:
            break
        i += 1
    return (dzisiaj + timedelta(days=i)).strftime('%Y-%m-%d')
# Sprawdzamy, czy dzisiaj jest dniem roboczym

####
### dane testowe: 
# blad brak polaczenia 

#A="Olsztyn Likusy"
#B="Ostrawa Gł./Ostrava hl.n."

## Trasa z przesiadka
A= "Gdańsk Główny"
B= "Kraków Główny"

date = GetNextDay(dzisiaj,pl_holidays)
times = "10:30"
# Stage 2 
imie = "Jan"
nazwisko = "Kowalski"
email = "jan.kowalski@example.com"
### kontener
tabelaczasow = []
global Logi
Logi = []
#### Konfig 
### Funkcja sprawdzajaca czy strona odrzuca polaczenie
def check_for_access_denied(driver):
    try:
        page_source = driver.page_source
        match = re.search(r"Access Denied", page_source)
        if match:
            Logi.append("wykryto komunikat Access Denied")
            return True
        else:
            return False
    except NoSuchElementException:
        return False

def WyjscieBledu(Komunikat,driver,log): # wyjscie bota po napotkaniu bledu
    global Logi
    global blad
    blad = Komunikat
    #print(Komunikat)
    Logi.append(log)
    now = datetime.now()
    a = now.strftime("%d_%H_%M")
    try:
        xe=f"Error_Ic/{str(a)}_blad_{str(blad)}.png"
        driver.save_screenshot(xe)
    except Exception as e:
        print("Wystąpił błąd podczas zapisywania zrzutów ekranu:", e)
    return False
##### Konfiguracja webdrivera oraz ustawienie liczników czasu
Logi.append(f"Bot Intercity nr { NR_BOTA} rozpoczyna działanie")
def initilize():
    global Logi
    global tabelaczasow
    tabelaczasow = [] # zresetowanie licznika czasu
    Logi.append(f"Inicjalizacja webdrivera bot intercity nr {NR_BOTA}")
    global driver
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920,1080)
    driver.set_window_position(-2000, 0)
    #driver.minimize_window()
    #driver.set_window_position(xsize, ysize)
    Logi.append(" inicjalizajca strony intercity")
    # ustawienie rozmiaru okna w pikselach (np. 800 pikseli szerokości i 600 pikseli wysokości)
    start_time = time.time()
    driver.get('https://www.intercity.pl/pl/')
    OczekiwanieWebDrivera=30# ile ma czekac webdriver na elementy w sekundach
    # Oblicz czas ładowania strony
    driver.execute_script("return window.onload")
    tabelaczasow.append(time.time() - start_time)
    # inicjalizacja waitera 
    global wait
    wait = WebDriverWait(driver, OczekiwanieWebDrivera)
    #driver.minimize_window()
global blad
blad = ""
def Intercity_Stage_1(A, B, date, times, driver, wait,tab): ## wyszukanie połączenia
    # kontener na bledy
    global blad
    # Wybór zaawansowanego wyszukiwania
    global Logi
    Logi.append("inicjalizacja wyszukiwania")
    start_time = time.time()
    try:
        try:
            Logi.append("Oczekiwanie na element 'a.btn-link.btn-adv-search ( Zaawansowane wyszukiwanie ))")
            s = time.time()
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.btn-link.btn-adv-search')))###
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn-link.btn-adv-search'))) ### ZMIANA  6-04-2023
            #print("Czas oczekiwania na element 'a.btn-link.btn-adv-search ( Zaawansowane wyszukiwanie ))", time.time() - s)
            element.click()
            Logi.append("udalo sie przejsc do zaawanasowanego wyszukiwania")
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
            print("Nie znaleziono elementu 'a.btn-link.btn-adv-search ( Zaawansowane wyszukiwanie )) oczekowano")
            print("Czas oczekiwania na element 'a.btn-link.btn-adv-search ( Zaawansowane wyszukiwanie ))", time.time() - s)
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                #print("Nie znaleziono elementu 'a.btn-link.btn-adv-search")
                blad="Nie znaleziono elementu 'a.btn-link.btn-adv-search"
                x = WyjscieBledu(blad,driver,blad)
                return False
        # wypełnienie pola Stacja Początkowa
        try:
            Logi.append("Oczekiwanie na element  (Stacja początkowa)")
            wait.until(EC.visibility_of_element_located((By.NAME, "stname[0]")))
            stacja_poczatkowa = driver.find_element(By.NAME, "stname[0]")
            stacja_poczatkowa.click()
            stacja_poczatkowa.clear()
            stacja_poczatkowa.send_keys(A)
            # Wybór stacji z listy
            clicker = wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@class='typeahead dropdown-menu']//a[contains(@title, '{A}')]")))
            clicker.click()
            Logi.append("udalo sie wybrac stacje poczatkowa")
            # wypełnienie pola Stacja Końcowa
            Logi.append("Wybór stacji koncowej")
            stacja_koncowa = driver.find_element(By.NAME, "stname[1]")
            stacja_koncowa.click()
            stacja_koncowa.clear()
            stacja_koncowa.send_keys(B)
            # wybór stacji z listy
            clicker = wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@class='typeahead dropdown-menu']//a[contains(@title, '{B}')]")))
            clicker.click()
            Logi.append("udalo sie wybrac stacje koncowa")
            # wypełnienie pola Data
            Logi.append("wypełnienie pola Data")
            data = driver.find_element(By.NAME, "date")
            data.click()
            data.clear()
            data.send_keys(date)
            Logi.append("udalo sie wypelnic pole Data")
            # wypełnienie pola Godzina
            Logi.append("wypełnienie pola Godzina")
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"input#ic-seek-time")))
            czas_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"input#ic-seek-time")))
            czas_element.click()
            czas_element.send_keys(Keys.CONTROL + "a") 
            czas_element.send_keys(Keys.DELETE) 
            czas_element.send_keys(times)
            czas_element.send_keys(Keys.ENTER)
            Logi.append("udało się wypełnić pole Godzina")
        except TimeoutException or NoSuchElementException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                blad="Nie znaleziono elementu do wypełnienia formularza"
                x = WyjscieBledu(blad,driver,blad)
                return False
        except:
            blad="Nie znaleziono elementu do wypełnienia formularza"
            x = WyjscieBledu(blad,driver,blad)
            return False
        ### Sprawdzenie poprawnosci wpisanych danych 
        try:
            Logi.append("Sprawdzenie poprawnosci wpisanych danych")
            if(stacja_poczatkowa.get_attribute("value") != A):
                ##print("Stacja początkowa nie zgadza się")
                blad = "Stacja początkowa nie zgadza się"
                Logi.append("Stacja początkowa nie zgadza się")
                x = WyjscieBledu(blad,driver,blad)
                return False
            if(stacja_koncowa.get_attribute("value") != B):
                blad = "Stacja końcowa nie zgadza się"
                ##print("Stacja końcowa nie zgadza się")
                x = WyjscieBledu(blad,driver,blad)
                return False
            if(data.get_attribute("value") != date):
                blad = "Data nie zgadza się"
                #print("Data nie zgadza się")
                return False
            selected_time_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ui-timepicker-wrapper ul.ui-timepicker-list li.ui-timepicker-selected')))
            if(selected_time_element.get_attribute('innerHTML') != times):
                #print(selected_time_element.get_attribute('innerHTML') ,times)
                #print("Czas nie zgadza się")
                return False
        except NoSuchElementException or TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                #print("Nie znaleziono elementu do sprawdzenia poprawności danych")
                blad="Nie znaleziono elementu do sprawdzenia poprawności danych"
                x = WyjscieBledu(blad,driver,blad)
                return False
        # kliknięcie przycisku Szukaj
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"button[name='search']")))
            szukaj = driver.find_element(By.CSS_SELECTOR,"button[name='search']")
            start_time = time.time()
            driver.execute_script("arguments[0].click();", szukaj)
        except NoSuchElementException or TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                #print("Nie znaleziono przycisku Szukaj")
                x = WyjscieBledu(blad,driver,blad)
                return False
        ## Czekanie na załadowanie strony i elementu "WYBIERZ"
        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH,('//li[@class="active"]//div[@msg="WYBIERZ"]')))) 
        except  TimeoutException:
            try:
                # obsługa przypadku nie znaleznienia połączenia 
                #element = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-warning") # daje bledy 
                element= driver.find_element(By.ID,"parent-ic-search-results")
                text = element.text
                #print(text)
                if text == "Nie znaleziono połączeń.":
                    #print("System Nie znalazl połączenia")
                    blad = "System Nie znalazl połączenia"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
                else:
                    raise NoSuchElementException
            except NoSuchElementException:
                # obsługa przypadku nie znaleznienia połączenia ale propozycji szukania nast dnia
                try:
                    success_alert = driver.find_element(By.CSS_SELECTOR,"div.alert.alert-success")
                    yes_button = driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary.pull-right")
                    yes_button.click()
                except  NoSuchElementException: ## dodac obsluge bledu Access Denied
                    if(check_for_access_denied(driver)):
                        blad = "Znaleziono komunikat Access Denied"
                        x = WyjscieBledu(blad,driver,blad)
                        return False
                    else:
                        blad="nieznany błąd przy ladowaniu strony po wyszukaniu"
                        x = WyjscieBledu(blad,driver,blad)
                        return False
        # mierzenie czasu ladowania strony
        driver.execute_script("return window.onload")
        tabelaczasow.append(time.time() - start_time)
        # Sprawdzenie czy wyszukiwanie się powiodło
        if("Bad Request" in driver.page_source):
            Logi.append("system odrzucił prosbe wyszukania")
            blad="system odrzucił prosbe wyszukania"
            return False
        Logi.append("Wyszukiwanie przebiegło pomyślnie")
        return True
    except:
        blad="nieznany błąd Stage_1"
        x = WyjscieBledu(blad,driver,blad)
        return False
def Intercity_Stage_2(imie,nazwisko,email,driver,wait): ## wybór połączenia oraz złozenie zamówienia
    global blad
    ## kliknięcie jednego przycisku "wybierz" \
    try:
        try:
            Logi.append( " Czekanie na załadowanie przycisku WYBIERZ")
            buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH,('//li[@class="active"]//div[@msg="WYBIERZ"]')))) 
        except TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                Logi.append( "Nie znaleziono przycisku WYBIERZ")
                blad="nieznany błąd przy ladowaniu strony po wyszukaniu"
                x = WyjscieBledu(blad,driver,blad)
                return False
        try:
            Logi.append( "Kliknięcie przycisku WYBIERZ")
            for button in buttons:
                Logi.append( " sprawdzam czy przycisk ma atrybut przesiadka")
                if(button.get_attribute("przesiadka")):
                    Logi.append( " przycisk ma atrybut przesiadka")
                    flag =1 
                    button.click()
                    break
                else:
                    Logi.append( " przycisk nie ma atrybutu przesiadka")
                    button.click()
                    break
        except :
            blad="nieznany błąd przy ladowaniu polaczen"
            x = WyjscieBledu(blad,driver,blad)
            return False
        # przescrolluj do przycisku "dalej"
        try:
            Logi.append( "Przescrolluj do przycisku Dalej")
            button1 = wait.until(EC.presence_of_element_located((By.ID, "strefa_modal")))
        #driver.execute_script("arguments[0].scrollIntoView();", button1)
        # kliknij przycisk "dalej"
            start_time = time.time()
            driver.execute_script("arguments[0].click();", button1)
        # kliknij przycisk dalej
            loadmask = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loadmask")))
            ## obsluga przesiadek
            try: 
                select = Select(driver.find_element(By.CSS_SELECTOR,"#tr_liczba_osob_n_2 select#liczba_n_2"))
                select.select_by_index(1)
                Logi.append( "Wybrano przesiadke")
            except NoSuchElementException:
                pass
            Logi.append( "Wybrano przesiadke")
            button1 = wait.until(EC.element_to_be_clickable((By.ID, "strefa_modal")))
            driver.execute_script("return window.onload")
            tabelaczasow.append(time.time() - start_time)
            start_time = time.time()
            Logi.append( "Klikam przycisk dalej")
            button1.click()
        except NoSuchElementException or TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                blad="Nie znaleziono przycisku dalej 1"
                x = WyjscieBledu(blad,driver,blad)
                return False
        # dodana opcja wykrycia przesiadki
        # wypełnij pole imie i nazwisko
        try:
            Logi.append( " szukam pola imie i nazwisko")
            button2 = wait.until(EC.presence_of_element_located((By.ID, "imie_nazwisko_podroznego")))
            driver.execute_script("return window.onload")
            tabelaczasow.append(time.time() - start_time)
            Logi.append( " wypełniam pole imie i nazwisko")
            button2.click()
            button2.send_keys("Jan Kowalski")
            Logi.append( " wypełniono pole imie i nazwisko")
        except TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                #print("Nie znaleziono pola imie i nazwisko")
                blad="Nie znaleziono pola imie i nazwisko"
                x = WyjscieBledu(blad,driver,blad)
                return False
        # kliknij przycisk dalej
        try:
            Logi.append( " szukam przycisku dalej 2")
            button3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".kup_bilet_button.blue_bg")))
            start_time = time.time()
            Logi.append( " klikam przycisk dalej 2")
            button3.click()
            driver.execute_script("return window.onload")
            tabelaczasow.append(time.time() - start_time)
            Logi.append( " kliknieto przycisk dalej 2")
            Logi.append( " szukam przycisku  kup bez rejestracji")
            button4 = driver.find_element(By.CSS_SELECTOR,'a.greylink[href="/konto_gosc_rejestracja.jsp?"]') ## 'a.greylink[href="/konto_gosc_rejestracja.jsp?"]'
            button4.click()
            Logi.append( " kliknieto przycisk kup bez rejestracji")
        except NoSuchElementException or TimeoutException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                blad="Nie znaleziono przycisku dalej 2 "
                x = WyjscieBledu(blad,driver,blad)
                return False
        # wypelnij pola formularza
        try:
            Logi.append( "wypelniam pola formularza")
            driver.find_element(By.NAME,"imie").send_keys(imie)
            driver.find_element(By.NAME,"nazwisko").send_keys(nazwisko)
            driver.find_element(By.NAME,"email").send_keys(email)
            driver.find_element(By.NAME,"powt_email").send_keys(email)
            Logi.append(    "wypelniono pola formularza")
        except NoSuchElementException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                    blad = "Nie znaleziono pola formularza"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
        # kliknij informacje o polityce prywatnosci
        try:
            Logi.append( "kliknam przycisk polityka prywatnosci")
            driver.find_element(By.ID,"akceptacja").click()
            Logi.append( "kliknieto przycisk polityka prywatnosci")
        except NoSuchElementException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                Logi.append( "Nie znaleziono przycisku akceptacji polityki prywatnosci")
                blad = "Nie  znaleziono przycisku akceptacji polityki prywatnosci"
                x = WyjscieBledu(blad,driver,blad)
                return False
        # kliknij przycisk "dalej" 
        try:
            Logi.append( "kliknam przycisk dalej 3")
            button = driver.find_element(By.XPATH,'//input[@name="actlogin" and @value="Dalej"]')
            driver.execute_script("arguments[0].scrollIntoView();", button)
            start_time = time.time()
            button.click()
            Logi.append( "kliknieto przycisk dalej 3")
            driver.execute_script("return window.onload")
            tabelaczasow.append(time.time() - start_time)
        except NoSuchElementException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                blad = "Nie znaleziono przycisku dalej 3"
                x = WyjscieBledu(blad,driver,blad)
                return False
        try: 
            Logi.append( "kliknam przycisk Zatwierdz")
            driver.find_element(By.XPATH, '//input[@name="actlogin" and @value="Zatwierdź"]').click()
        except NoSuchElementException:
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                blad = "Nie znaleziono przycisku zatwierdz"
                x = WyjscieBledu(blad,driver,blad)
                return False    
        try:
            Logi.append( "kliknieto przycisk zatwierdz")
            button = wait.until(EC.presence_of_element_located((By.ID, "platosc_fieldset_4")))
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
        except NoSuchElementException or TimeoutException:
            try:
                text_to_find = 'Możliwość rezerwacji została zablokowana, ponieważ pięć dokonanych przez Ciebie transakcji nie zostało zakończonych płatnością.  Sprawdź Regulamin e-IC.'
                element = driver.find_element(By.XPATH,"//td[contains(text(), '{}')]".format(text_to_find))
                Logi.append( "system zablokował mozliwosc rezerwacji przez przekroczenie limitu 5 transakcji")
                blad = "system zablokował mozliwosc rezerwacji przez przekroczenie limitu 5 transakcji"
                x = WyjscieBledu(blad,driver,blad)
                return True 
            except NoSuchElementException:
                if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
                else:
                    blad = "Nie znaleziono przycisku wyboru platnosci"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
        try:
            Logi.append( " Klikam przycisk kupuje i place")
            button = wait.until(EC.element_to_be_clickable((By.ID, "pay_button")))#
            start= time.time()
            if button.is_enabled():
                button.click()
        except NoSuchElementException:
            blad = "Nie znaleziono przycisku kupuje i place"
            x = WyjscieBledu(blad,driver,blad)
            return False
        try:
            wait.until(EC.url_contains('przelewy24'))
            if 'przelewy24' in driver.current_url:
                Logi.append( "przekierowanie na przelewy24 zadziałało prawidłowo")
                driver.execute_script("return window.onload")
                tabelaczasow.append(time.time() - start)
                driver.close()
                Logi.append( f"Zakonczono test pomyslnie dla bota nr {NR_BOTA}")
                print(f"Bot  Intercity  nr {NR_BOTA} pomyslnie zlozył zamówienie na Intercity.pl")
                return True
            else:
                blad = "przycisk przekierowania nie zadziałał prawidłowo"
                x = WyjscieBledu(blad,driver,blad)
                return False
        except NoSuchElementException or UnexpectedAlertPresentException or TimeoutException:  ## Spytac sie jak powinno to obsłuzyc 
            if(check_for_access_denied(driver)):
                    blad = "Znaleziono komunikat Access Denied"
                    x = WyjscieBledu(blad,driver,blad)
                    return False
            else:
                #print("Nie znaleziono przycisku  kupuje i place")
                blad = "Nie znaleziono przycisku kupuje i place"
                x = WyjscieBledu(blad,driver,blad)
                return False
    except Exception as e :
        blad = "Nieznany blad stage_2" + str(e) 
        x = WyjscieBledu(blad,driver,blad)
        return False

def ender(): ## funkcja zamykajaca program z bledem
        print(f"Bot Intercity nr :{NR_BOTA} napotkal blad " + str(blad) + "  \n")
        Logi.append(f"Bot Intercity nr :{NR_BOTA} napotkal blad " + str(blad) + "  \n")
integral=int(internal_error)

a=1
while(a <= integral):
    #print(a <= integral and a >= 0)
    #print("intercity bot nr " + str(NR_BOTA) + "  \n" + "test nr " + str(a) + "  \n")
    Logi.append(f"======== Rozpoczynam test nr {a} dla bota intercity nr {NR_BOTA} =======")
    start_time_stage_1=time.time()
    try:
        initilize()
        Stage_1=Intercity_Stage_1(A,B,date,times,driver,wait,tabelaczasow)
        end_time_stage_1=time.time()
        loading_time_stage_1 = end_time_stage_1 - start_time_stage_1
    except Exception as e :
        Logi.append("Nieznany blad stage_1")
        blad = "Znaleziono komunikat: " + str(e)
        a+=1
        x = WyjscieBledu(blad,driver,blad)
        continue
    start_time_stage_2=time.time()
    if(Stage_1==True):
        global Stage_2
        Stage_2=Intercity_Stage_2(imie,nazwisko,email,driver,wait)
        end_time_stage_2=time.time()
        loading_time_stage_2 = end_time_stage_2- start_time_stage_2
        if(Stage_2):
            with open(output_file, "w") as file:
                #print("zapisywanie informacji do pliku") 
                #print(len(tabelaczasow))
                file.write(str(loading_time_stage_1) + "\n")
                file.write(str(loading_time_stage_2) + "\n")
                for x in tabelaczasow:
                    file.write(str(x) + "\n")
            fileu=f"Logi_Bot\\Log_Intercity_{NR_BOTA}.txt"
            with open(fileu, "w") as file:
                    for x in Logi:
                        file.write(str(x) + "\n")
            sys.exit()
            
        else:
            a+=1
    else:
        a+=1
if(a>=int(internal_error)):
    ender()

fileu=f"Logi_Bot\\Log_Intercity_{NR_BOTA}.txt"
with open(fileu, "w") as file:
        for x in Logi:
            file.write(str(x) + "\n")
sys.exit()

