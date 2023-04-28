import numpy as np

# Dane wejściowe XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# Oczekiwane wyjście XOR
y = np.array([[0], [1], [1], [0]])

# Inicjalizacja wag losowo
np.random.seed(0)
W1 = np.random.randn(2, 2)  # Wagi dla warstwy ukrytej
W2 = np.random.randn(2, 1)  # Wagi dla warstwy wyjściowej

# Stała uczenia
learning_rate = 0.1
# Funkcja aktywacji sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Pochodna funkcji aktywacji sigmoid
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))
# Trening sieci neuronowej
for epoch in range(5000):
    for i in range(len(X)):
        # Przejście do przodu
        x = X[i]
        z1 = np.dot(x, W1)
        a1 = sigmoid(z1)
        z2 = np.dot(a1, W2)
        a2 = sigmoid(z2)

        # Obliczenie błędu
        error = y[i] - a2

        # Propagacja wsteczna
        delta_output = error * sigmoid_derivative(z2)
        delta_hidden = np.dot(delta_output, W2.T) * sigmoid_derivative(z1)

        # Aktualizacja wag
        W2 += learning_rate * np.outer(a1, delta_output)
        W1 += learning_rate * np.outer(x, delta_hidden)
for epoch in range(5000):
    for i in range(len(X)):
        # Przejście do przodu
        x = X[i]
        z1 = np.dot(x, W1)
        a1 = sigmoid(z1)
        z2 = np.dot(a1, W2)
        a2 = sigmoid(z2)

        # Obliczenie błędu
        error = y[i] - a2

        # Propagacja wsteczna
        delta_output = error * sigmoid_derivative(z2)
        delta_hidden = np.dot(delta_output, W2.T) * sigmoid_derivative(z1)

        # Aktualizacja wag
        W2 += learning_rate * np.outer(a1, delta_output)
        W1 += learning_rate * np.outer(x, delta_hidden)
for epoch in range(5000):
    for i in range(len(X)):
        # Przejście do przodu
        x = X[i]
        z1 = np.dot(x, W1)
        a1 = sigmoid(z1)
        z2 = np.dot(a1, W2)
        a2 = sigmoid(z2)

        # Obliczenie błędu
        error = y[i] - a2

        # Propagacja wsteczna
        delta_output = error * sigmoid_derivative(z2)
        delta_hidden = np.dot(delta_output, W2.T) * sigmoid_derivative(z1)

        # Aktualizacja wag
        W2 += learning_rate * np.outer(a1, delta_output)
        W1 += learning_rate * np.outer(x, delta_hidden)
for epoch in range(50000):
    for i in range(len(X)):
        # Przejście do przodu
        x = X[i]
        z1 = np.dot(x, W1)
        a1 = sigmoid(z1)
        z2 = np.dot(a1, W2)
        a2 = sigmoid(z2)

        # Obliczenie błędu
        error = y[i] - a2

        # Propagacja wsteczna
        delta_output = error * sigmoid_derivative(z2)
        delta_hidden = np.dot(delta_output, W2.T) * sigmoid_derivative(z1)

        # Aktualizacja wag
        W2 += learning_rate * np.outer(a1, delta_output)
        W1 += learning_rate * np.outer(x, delta_hidden)
test_input = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
test_output = sigmoid(np.dot(sigmoid(np.dot(test_input, W1)), W2))
print("Wagi dla warstwy ukrytej:")
print(W1)
print("Wagi dla warstwy wyjściowej:")
print(W2)
print("Przewidywane wyjście dla danych testowych:")
print(test_output)
scripts\pyinstaller.exe --onefile serwis.py --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Bot\test.py;Bot" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Bot\bilkom.py;Bot" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Bot\Debbug.py;Bot" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\templates\index.html;templates" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Billkomdane.csv;." --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\dane.csv;." --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\config.ini;." --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Log;Log" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\Logi_Bot;Logi_Bot" --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\requirements.txt;." --add-data "C:\Users\zedko\Desktop\Python-PKP\PKP-BOT-Jeze-Tuptusie\1.wav" 
