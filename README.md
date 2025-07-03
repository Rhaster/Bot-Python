# Aplikacja do sterowania i monitorowania botów Intercity i Bilkom

## Opis ogólny
Aplikacja służy do zdalnego uruchamiania i nadzoru pracy dwóch botów: **Intercity** oraz **Bilkom**.  
Backend projektu został zaimplementowany w Pythonie i zawiera skrypty (`bilkom.py`, `Debbug.py`, `test.py`) odpowiedzialne za logikę uruchamiania, testowania i monitorowania botów.  
Część front‑endową stanowią statyczne strony HTML (`index.html`, `dioda.html`, `plot.html`), które zapewniają interfejs użytkownika oparty na przeglądarce internetowej.  
Dzięki aplikacji można kompleksowo zarządzać pracą botów oraz wizualizować ich status i wyniki działania.

## Główne funkcjonalności
- **Równoczesne uruchamianie wielu botów** – aplikacja umożliwia jednoczesne uruchomienie wielu instancji botów w różnych trybach pracy.  
- **Konfiguracja trybu i powtórzeń** – przed uruchomieniem botów można wybrać tryb działania (np. testowy czy produkcyjny) oraz liczbę powtórzeń zadania.  
- **Wizualizacja statusu i danych** – system zbiera dane z działania botów i prezentuje je w postaci przejrzystych wykresów aktualizowanych na żywo.  
- **Kolorowe wskaźniki diodowe** – interfejs wykorzystuje kolorowe diody LED (zielona, żółta, czerwona) do sygnalizacji aktualnego stanu każdego bota.

## Interfejs webowy
Interfejs użytkownika zbudowano w HTML i JavaScript (jQuery) oraz wykorzystano bibliotekę **Plotly** do tworzenia wykresów.

| Strona | Zawartość |
| ------ | ---------- |
| `index.html` | Formularz do wprowadzania parametrów (liczba botów, powtórzenia, tryb), przyciski **Start/Stop**, ogólny status systemu. |
| `dioda.html` | Kolorowe diody LED wskazujące stan botów (zielony – OK, żółty – ostrzeżenie, czerwony – błąd). |
| `plot.html` | Interaktywne wykresy prezentujące statystyki — np. czasy odpowiedzi czy liczbę przetworzonych zadań. |

## Technologie
- **Python** – logika botów i backend.  
- **Flask** – serwer HTTP i API dla front‑endu.  
- **HTML / CSS** – struktura i styl interfejsu.  
- **JavaScript (jQuery)** – obsługa zdarzeń po stronie klienta.  
- **Plotly.js** – interaktywne wykresy.  

## Autor
Paweł Deptuła
