import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os
import sys 
import time
import psutil
import pandas as pd
import datetime as dt
############# Definicje do interpretera
proj_di = sys.argv[6]
# Względna ścieżka do interpretera Pythona
Interpreter = os.path.join(proj_di, 'Scripts', 'python.exe')
# Względna ścieżka do skryptu bilkom.py
Billkom = os.path.join(proj_di, 'Bot', 'bilkom.py')
# Względna ścieżka do skryptu Debbug.py
Intercity = os.path.join(proj_di, 'Bot', 'Debbug.py')
# Względna ścieżka do katalogu Logi_Bot
Logi_Bot = os.path.join(proj_di, 'Logi_Bot')
# Względna ścieżka do katalogu Log
Log  = os.path.join(proj_di, 'Log')
###############################################
## Czyszczenie po poprzednich przebiegach
print("czyszczenie po poprzednich przebiegach")
folders_to_clear = [Logi_Bot, Log] ### tu wklejyc sciezke do folderu z logami botów 
for folder in folders_to_clear:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'nie usunieto {file_path}.  {e}')
n_intercity=int(sys.argv[1])# ilosc botow dla intercity 
n_bilkom =int(sys.argv[2])# ilosc botow dla bilkom 
check = int(sys.argv[3]) # tryb bota ic+bilkom, ic, bilkom
internal_error_billkom = int(sys.argv[5])## ilosc prób bota przed zakonczeniem
internal_error_intercity = int(sys.argv[4])## ilosc prób bota przed zakonczeniem
print("Wybrane Parametry wejsciowe:")
print("Ilosc botow dla intercity: ",n_intercity,"ilość powtórzeń bota w razie niepowodzenia: ",internal_error_intercity)
print("Ilosc botow dla bilkom: ",n_bilkom,"ilość powtórzeń bota w razie niepowodzenia: ",internal_error_billkom)
print("Wybrano case: ",check)
if( check == 1 or check == 3):
    df = pd.read_csv('BillkomDane.csv', sep=',') # nazwa_pliku to nazwa twojego pliku csv
    selected_rows = {}
    for przewoznik in set(df['Przewoźnik']):
        selected_rows[przewoznik] = df[df['Przewoźnik'] == przewoznik].sample(n=1)
    global Holder
    Holder = [[] for x in range(len(selected_rows))]
    h = 0
    for przewoznik, row in selected_rows.items():
        #print(f'{przewoznik}:')
        #print(row)
        Holder[h].append(row.values.tolist())
        if(len(Holder)==n_bilkom-1):
            break
        h += 1
    for hold in Holder:
        print(hold)
######### Intercity #########
Faza_1 = [] 
Faza_2 = [] 
Strona_glowna= [] 
Wynik_wyszukiwania = [] 
Wybor_pociagu = [] 
Wybor_miejsca= [] 
Podsumowanie= [] 
Zamowienie = [] 
Platnosc = []
global lists
lists = [Faza_1, Faza_2, Strona_glowna, Wynik_wyszukiwania, Wybor_pociagu, Wybor_miejsca, Podsumowanie, Zamowienie, Platnosc]
########################
######### Bilkom #########
Strona_1=[]
Strona_2 = []
Strona_3 = []
Strona_4 = []
Czas_Bota=[]
lists_bilkom = [Strona_1, Strona_2, Strona_3, Strona_4, Czas_Bota]
########################
W=0
a=0
numbers = []
procarray=[]
# Specjalny case dla jednego bota intercity i n bilkom
if(check == 1):
    print("Uruchamianie botów Intercity i Bilkom")
    for i in range(n_intercity):
        filename = f"Log\\czasy_Intercity_{i}.txt"  # unikalna nazwa pliku dla każdej instancjiHolder[i][0][0][0]) # 3 to kolumna "Do" w DataFrame  2 to kolumna "Z" w DataFrame # 0 to kolumna "Przewoźnik" w DataFrame 
        f = open(filename, "a")  
        try:
            proc = subprocess.Popen([Interpreter, 
                                     Intercity, 
                                     filename,str(i),str(internal_error_intercity)])
            time.sleep(2)  # opóźnienie, aby proces miał czas na utworzenie pliku
            procarray.append(proc)
        except subprocess.CalledProcessError as exc:
            print(f"Proces botów nr {i} Intercity sie nie uruchomil. "f"Returned {exc.returncode}\n{exc}")
    for i in range(n_bilkom):
        print(f" Sprawdzane polaczenia bot Billkom nr {i}: {Holder[i][0][0][2]} {Holder[i][0][0][3]}")# type ignore
        filename1 = f"Log\\czasy_Bilkom_{i}.txt"  # unikalna nazwa pliku dla każdej instancji
        t = open(filename1, "a")
        try:
            proc1 = subprocess.Popen([Interpreter,
                                      Billkom, filename1,str(i),str(Holder[i][0][0][2]),str(Holder[i][0][0][3]),str(internal_error_billkom)])
            time.sleep(2)  # opóźnienie, aby proces miał czas na utworzenie pliku
            procarray.append(proc1)
        except subprocess.CalledProcessError as exc:
            print(f"Proces botów nr {i} Bilkom sie nie uruchomil. "f"Returned {exc.returncode}\n{exc}")

if(check == 3):
### Bilkom ### wywołanie procesuvv
    print("Uruchamianie botów Bilkom")
    for i in range(n_bilkom):
        filename = f"Log\\czasy_Bilkom_{i}.txt"  # unikalna nazwa pliku dla każdej instancji
        f = open(filename, "a")
        try:
            proc = subprocess.Popen([Interpreter, 
                                     Billkom, 
                                     filename,str(i),str(Holder[i][0][0][2]),str(Holder[i][0][0][3]),str(internal_error_billkom)])
            time.sleep(0.2)  # opóźnienie, aby proces miał czas na utworzenie pliku
            procarray.append(proc)
        except subprocess.CalledProcessError as exc:
            print(f"Proces sie nie uruchomil "f"Returned {exc.returncode}\n{exc}")
if(check == 2):
    print("Uruchamianie botów Intercity")
    for i in range(n_intercity):
        filename = f"Log\\czasy_Intercity_{i}.txt"  # unikalna nazwa pliku dla każdej instancji
        f = open(filename, "a")  
        try:
            proc = subprocess.Popen([Interpreter, 
                                     Intercity, filename,str(i),str(internal_error_intercity)])
            time.sleep(1)  # opóźnienie, aby proces miał czas na utworzenie pliku
            procarray.append(proc)
        except subprocess.CalledProcessError as exc:
            print(f"Proces nr {i} intercity sie nie uruchomil "f"Returned {exc.returncode}\n{exc}")
print("Procesy uruchomione czekanie na zakonczenie")
for x in procarray:
    x.wait()
print("Boty zakonczyly dzialanie")
### Intercity ### odczyt danych
if(check ==1 or check == 2):
    print("Inicjowanie Odczytu danych Intercity")
    for i in range(n_intercity):
        filename = f"Log\\czasy_Intercity_{i}.txt"  # unikalna nazwa pliku dla każdej instancji
        try:
            if os.path.getsize(filename) == 0:
                print(f"Intercity nr {i} :Plik jest pusty.")
            else:
                with open(filename, 'r') as file:
                    for line in file:
                        #print(W)
                        lists[W].append(float(line.strip()))
                        W += 1
        except FileNotFoundError:
            pass
        #print(f"iteracja nr {a}")
        #print(lists)
        a += 1
        W = 0
    if not lists:
        print("Lista jest pusta. Zaden bot Intercity nie ukonczyl dzialania pomyslnie.")
        if(check == 2):
            exit()
    ### zapisanie danych do pliku Intercity ###
    with open("CzasyWszystkie_Intercity.txt", 'a') as file:
        for x in lists:
            file.write(str(x))
            file.write("\n")
### Bilkom ### odczyt danych
if(check ==1 or check == 3):
    print("Inicjowanie Odczytu danych Bilkom")
    for i in range(n_bilkom):
        #print("Odczyt danych")
        filename = f"Log\\czasy_Bilkom_{i}.txt"  # unikalna nazwa pliku dla każdej instancji
        if os.path.getsize(filename) == 0:
            print(f"Bilkom nr {i} : Plik jest pusty.")
        else:
            with open(filename, 'r') as file:
                for line in file:
                    #print(W)
                    lists_bilkom[W].append(float(line.strip()))
                    W += 1
        #print(f"iteracja nr {a}")
        #print(lists)
        a += 1
        W = 0
### zapisanie danych do pliku Bilkom ###
    with open("CzasyWszystkie_Bilkom.txt", 'a') as file:
        for x in lists_bilkom:
            file.write(str(x))
            file.write("\n")    
    if not lists_bilkom:
        print("Lista jest pusta. Zaden bot Bilkom nie ukonczyl dzialania pomyslnie.")
        if(check == 3):
            exit()
#### dane do wizualizacji Intercity ####
text=[ "Faza_1", "Faza_2", "Strona_glowna", "Wynik_wyszukiwania", "Wybor_pociagu", "Wybor_miejsca", "Podsumowanie", "Zamowienie","Platnosc"]
j=0
srednie=[]
width = 0.35
fig1 = plt.figure(figsize=(12, 6))
h=0
#### dane do wizualizacji Bilkom ####
text_bilkom=[ "Strona_1", "Strona_2", "Strona_3", "Strona_4"," Czas_Bota"]
srednie_bilkom=[]
####
fig, (ax1, ax2) = plt.subplots(1, 2)
if(check ==1 or check == 2):
    ax1.set_title("Próby Intercity")
    ax1.set_yticks(np.arange(0, n_intercity+1, 1))
    ax1.bar(1, len(lists[0]), color='green', width=width, label='ilość prób')
    ax1.bar(1 + width , n_intercity - len(lists[0]), color='red', width=width, label='ilość prób')
if(check ==1 or check == 3):
    ax2.set_title("Próby Bilkom")
    ax2.set_yticks(np.arange(0, n_bilkom+1, 1))
    ax2.bar(1, len(lists_bilkom[0]), color='green', width=width, label='ilość prób')
    ax2.bar(1 + width , n_bilkom - len(lists_bilkom[0]), color='red', width=width, label='ilość prób1')
if(check ==1 or check == 2):
    if(lists[0]):
        print("Inicjowanie: wykresy  Intercity")
        for x in lists:
            srednie.append(np.nanmean(x))
            srednie[h]=round(srednie[h],3)
            h+=1
        for i in range(len(lists)):
            for j in range(len(lists[i])):
                lists[i][j] = round(lists[i][j], 4)
        j=0
        if(srednie):
            print(srednie)
            for title, data in zip(text, lists):
                if(data):
                    if(j==0): # wykres sredniej dla kazdej operacji 
                        ranger = np.arange(0, int(np.ceil(max(srednie))) + 1, 1)
                        fig1 = plt.figure(figsize=(12, 6))
                        ax = fig1.add_subplot(111) # type: ignore
                        ax.bar(text, srednie, color='royalblue', width=width, label='Średnie czasy')
                        ax.set_yticks(ranger)
                        ax.grid(color='Red', linestyle='--', linewidth=1, axis='y', alpha=0.7)
                        ax.set_title(label='Średnie czasy Intercity', loc='center', fontsize=20, fontweight='bold', color='black')
                        for i, v in enumerate(srednie):
                            ax.text(i - 0.15, v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                        ax.legend()
                        j+=1
                    # wykresy dla kazdej operacji
                    fig2 = plt.figure(figsize=(12, 6))
                    ranger = np.arange(0, int(np.ceil(max(data))) + 1, 1)
                    zakres = np.arange(0, len(data), 1)
                    sred=[srednie[j-1]] * len(zakres)
                    ax = fig2.add_subplot(111) # type: ignore
                    ax.bar(zakres, data, color='royalblue', width=width, label='Czas wykonania')
                    ax.bar(zakres + width , sred, color='orange', width=width, label='Sredni czas')
                    ax.set_yticks(ranger)
                    ax.set_xticks(zakres)
                    ax.set_title(label=title)
                    for i, v in enumerate(sred):
                        ax.text(i + 0.25, v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                    for i, v in enumerate(data):
                        ax.text(i - 0.05 , v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                    ax.legend()
                    ax.set_title(label=title + " Intercity")
                    ax.set_ylabel(" Czas [s]")
                    ax.set_xlabel("Nr podejscia")
                    j+=1
    else:
        print("Boty Intercity nie zdołały wykonać zadania")
        print("Wykresy nie zostaną wygenerowane")
h=0
if(check ==1 or check == 3):
    if(lists_bilkom[0]):
        print("Inicjowanie : wykresy Bilkom")
        for x in lists_bilkom:
            srednie_bilkom.append(np.nanmean(x))
            srednie_bilkom[h]=round(srednie_bilkom[h],4)
            h+=1
        for i in range(len(lists_bilkom)):
            for j in range(len(lists_bilkom[i])):
                lists_bilkom[i][j] = round(lists_bilkom[i][j], 4)
        j=0
        if(srednie_bilkom):
            print(srednie_bilkom)
            for title, data in zip(text_bilkom, lists_bilkom):
                if(j==0): # wykres sredniej dla kazdej operacji 
                    ranger = np.arange(0, int(np.ceil(max(srednie_bilkom))) + 1, 1)
                    fig1 = plt.figure(figsize=(12, 6))
                    ax = fig1.add_subplot(111) # type: ignore
                    ax.bar(text_bilkom, srednie_bilkom, color='royalblue', width=width, label='Średnie czasy')
                    ax.set_yticks(ranger)
                    ax.grid(color='Red', linestyle='--', linewidth=1, axis='y', alpha=0.7)
                    ax.set_title(label='Średnie czasy Bilkom')
                    for i, v in enumerate(srednie_bilkom):
                        ax.text(i - 0.15, v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                    ax.legend()
                    j+=1
                # wykresy dla kazdej operacji
                fig2 = plt.figure(figsize=(12, 6))
                ranger = np.arange(0, int(np.ceil(max(data))) + 1, 1)
                zakres = np.arange(0, len(data), 1)
                sred=[srednie_bilkom[j-1]] * len(zakres)
                ax = fig2.add_subplot(111) # type: ignore
                ax.bar(zakres, data, color='royalblue', width=width, label='Czas wykonania')
                ax.bar(zakres + width , sred, color='orange', width=width, label='Sredni czas')
                ax.set_yticks(ranger)
                ax.set_xticks(zakres)
                ax.set_title(label=title)
                for i, v in enumerate(sred):
                    ax.text(i + 0.25, v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                for i, v in enumerate(data):
                    ax.text(i - 0.05 , v + 0.05 , str(v)+"s", color='black', fontweight='bold')
                ax.legend()
                ax.set_ylabel(" Czas [s]")
                ax.set_xlabel("Nr podejscia")
                ax.set_title(label=title + " Bilkom")
                j+=1
    else:
        print(" Boty Bilkom nie zdołały wykonać zadania")
        print("Wykresy nie zostaną wygenerowane")
#zapis figur do pliku
def save_image(filename):
    p = PdfPages(filename)
    fig_nums = plt.get_fignums()  
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs: 
        fig.savefig(p, format='pdf')  # type: ignore
    p.close()  
if(lists[0] or lists_bilkom[0]):
    now = dt.datetime.now()
    #filename = now.strftime("%Y-%m-%d-%H-%M-%S.pdf")
    filename="Raport.pdf"
    save_image(filename)  
    print("Zapisano raport do pliku: ", filename) 
else:
    print("wszystkie boty nie zdołały wykonać zadania")
## usuwanie plików
if(check == 1 or check == 2 or check ==0):
    for p in range(n_intercity):
        file_path = f"Log\\czasy_Intercity_{p}.txt"  # unikalna nazwa pliku dla każdej instancji
        if any(process.name() == "python" and file_path in process.open_files() for process in psutil.process_iter()):
            for process in psutil.process_iter():
                if process.name() == "python" and file_path in process.open_files():
                    process.terminate()
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        time.sleep(1)
        else:
            try:
                os.remove(file_path)
            except PermissionError:
                time.sleep(1)
        try:
            os.remove(file_path)
        except PermissionError:
            time.sleep(1)
        except FileNotFoundError:
            continue
    print("usunieto pliki intercity")
if(check == 1 or check == 3 or check ==0):
    for p in range(n_bilkom):
            file_path1 = f"Log\\czasy_Bilkom_{p}.txt" 
            if any(process.name() == "python" and file_path1 in process.open_files() for process in psutil.process_iter()):
                for process in psutil.process_iter():
                    if process.name() == "python" and file_path1 in process.open_files():
                        process.terminate()
                        try:
                            os.remove(file_path1)
                        except PermissionError:
                            time.sleep(1)
            else:
                try:
                    os.remove(file_path1)
                except PermissionError:
                    time.sleep(1)
            if os.path.exists(file_path1):
                try:
                    os.remove(file_path1)
                except PermissionError:
                        time.sleep(1)
    print("usunieto pliki intercity")
print("zapis wyniku do pliku")
if(check == 1 or check == 2):
    Wynik = "Wynik_intercity.txt"
    if(len(lists[0])==n_intercity):
        with open(Wynik, "w") as file:
            file.write(str(1) + "\n")
    else:
        with open(Wynik, "w") as file:
            file.write(str(0) + "\n")
if(check == 1 or check == 3 ):
    Wynik = "Wynik_billkom.txt"
    if(len(lists_bilkom[0])==n_bilkom):
        with open(Wynik, "w") as file:
            file.write(str(1) + "\n")
    else:
        with open(Wynik, "w") as file:
            file.write(str(0) + "\n")
from datetime import datetime
now = datetime.now()
timer = now.strftime("%H:%M:%S")
df = pd.DataFrame(dict(date=([timer]*4), value=[len(lists[0]),n_intercity - (len(lists[0])),len(lists_bilkom[0]),n_bilkom-len(lists_bilkom[0])])) # utworzenie dataframe z datami i wartościami
df.to_csv('dane.csv', index=False)
exit()
