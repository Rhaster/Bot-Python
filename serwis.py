
import winsound
from flask import Flask, Response, make_response, render_template, request, jsonify
import subprocess
import plotly
import plotly.graph_objs as go
import sys
import os
import threading
import time
import random
from datetime import datetime
import datetime  as dt
import pandas as pd 
import json
from bs4 import BeautifulSoup
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)
#################### Definicje DO Interpretera ####################v
Interpreter = 'C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Scripts\\python.exe'
Test_py="C:\\Users\\zedko\\Desktop\\Python-PKP\\PKP-BOT-Jeze-Tuptusie\\Bot\\test.py"
audio_file = "1.wav"
###################################################################
global fig
fig = go.Figure()

@app.route('/activate', methods=['POST'])
def activate():
    print("activate")
    global fig
    global data1, data2, data3, data4
    n_intercity = config.getint('intervals', 'n_intercity')
    n_bilkom = config.getint('intervals', 'n_bilkom')
    powt_intercity = config.getint('intervals', 'powt_intercity')
    powt_billkom = config.getint('intervals', 'powt_billkom')
    minutes = config.getint('intervals', 'minutes')

        # Wczytanie wartości z sekcji bot
    bot_mode = config.get('bot', 'bot_mode')
    now1 = datetime.now()
    timer = now1.strftime("%H:%M:%S")
    flaga=0
    while True:
        Start = time.time()
        if(bot_mode == "0" and flaga==1):
            time.sleep(1)
            print("aktywacja procesu Intercity + billkom")
            t=subprocess.Popen([Interpreter, 
                           Test_py, str(n_intercity), str(n_bilkom), str(1),str(powt_intercity),str(powt_billkom)])
            t.wait()
        elif(bot_mode == "1" and flaga==1):
            time.sleep(1)
            print("aktywacja procesu Intercity")
            t=subprocess.Popen([Interpreter, 
                           Test_py, str(n_intercity), str(n_bilkom), str(2),str(powt_intercity),str(powt_billkom)])
            t.wait()
        elif(bot_mode == "2" and flaga==1):
            time.sleep(1)
            print("aktywacja procesu Billkom")
            print("aktywacja billkom")
            t=subprocess.Popen([Interpreter, 
                           Test_py, str(n_intercity), str(n_bilkom), str(3)])
            t.wait()
        i=0
        print("Wywolanie botow trwalo", time.time()-Start , "sekund")
        if(flaga==0): # inicjalizacja wykresu
            print("tworze wykres")
            df = pd.DataFrame(dict(
                    date=([timer]*4),
                    value=[0, 0, 0, 0]
                ))
            #print(df)

            fig.add_trace(go.Scatter(
                x=[df['date'][0]],
                y=[df['value'][0]],
                mode="markers+lines",
                name="Intercity Sukces",fillcolor="blue"
            ))

            fig.add_trace(go.Scatter(
                x=[df['date'][1]],
                y=[df['value'][1]],
                mode="markers+lines",
                name="Intercity Niepowodzenie",fillcolor="red"
            ))

            fig.add_trace(go.Scatter(
                x=[df['date'][2]],
                y=[df['value'][2]],
                mode="markers+lines",
                name="Bilkom Sukces",fillcolor="green"
            ))

            fig.add_trace(go.Scatter(
                x=[df['date'][3]],
                y=[df['value'][3]],
                mode="markers+lines",
                name="Billkom Niepowodzenie",fillcolor="purple"
            ))
            layout = go.Layout(
                title='Wykres Ruchu Botów',
            plot_bgcolor='black',
                paper_bgcolor='gray',
                width=1280, height=1024,
            autosize=True ,
                    yaxis=dict(
                range=[0, 10],
                tick0=0,
                dtick=1
            )# dodaj właściwość responsywności
            )   
            fig.update_layout(layout
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
        else:
            print("aktualizuje wykres")
            df = pd.read_csv('dane.csv')
            #print(df)
            fig['data'][0]['x'] = list(fig['data'][0]['x']) + [df['date'][i]] # type: ignore
            fig['data'][0]['y'] = list(fig['data'][0]['y']) + [df['value'][i]]# type: ignore
            fig['data'][1]['x'] = list(fig['data'][1]['x']) + [df['date'][i]]# type: ignore
            fig['data'][1]['y'] = list(fig['data'][1]['y']) + [df['value'][i+1]]# type: ignore
            fig['data'][2]['x'] = list(fig['data'][2]['x']) + [df['date'][i]]# type: ignore
            fig['data'][2]['y'] = list(fig['data'][2]['y']) + [df['value'][i+2]]# type: ignore
            fig['data'][3]['x'] = list(fig['data'][3]['x']) + [df['date'][i]]# type: ignore
            fig['data'][3]['y'] = list(fig['data'][3]['y']) + [df['value'][i+3]]# type: ignore
            print("update lampek")
            try:
                with open("Wynik_intercity.txt", "r") as file:
                        Lines= file.readlines()
                with open("Wynik_billkom.txt", "r") as file:
                        Lines2= file.readlines()
                change_color(int(Lines[0]), int(Lines2[0]))
            except FileNotFoundError:
                print("Brak pliku")
                pass
            update_data()
        if(flaga==1):
            for x in range(minutes*60):
                time.sleep(1)
                print("pozostało " + str((minutes*60) - x) + " sekund")
        else:
            flaga+=1

@app.route('/update_data')
def update_data():
    def generate():
        while True:
            # Pobierz aktualne dane wykresu
            fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            yield f"data: {fig_json}\n\n"
            time.sleep(1)

    return Response(generate(), mimetype="text/event-stream")
@app.route('/')
def home():
    #print("home")
    return render_template('index.html')

def change_color(x,y):
    if x == 1 and y == 1:
        color_x = 'green'
        color_y = 'green'
    elif x == 1 and y == 0:
        color_x = 'green'
        color_y = 'red'
        winsound.PlaySound(audio_file, winsound.SND_FILENAME)
    elif x == 0 and y == 1:
        color_x = 'red'
        color_y = 'green'
        winsound.PlaySound(audio_file, winsound.SND_FILENAME)
    else:
        color_x = 'red'
        color_y = 'red'
        winsound.PlaySound(audio_file, winsound.SND_FILENAME)
    change_colors("element_x", color_x)
    change_colors("element_y", color_y)
    return render_template('index.html')
def change_colors(element_id, color_id):
    print("zmieniam kolor led")
    with open("templates/index.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        element = soup.find(id=element_id)
        element["style"] = f"background-color: {color_id} ; width:50px; height:50px;" # type: ignore
    with open("templates/index.html", "w") as fp:
        fp.write(str(soup))
    return render_template('index.html')
@app.route('/stop', methods=['GET'])
def stop_server():
    print("Zatrzymuje Bota")
    change_colors("element_x", "blue")
    change_colors("element_y", "blue")
    os.system("taskkill /f /im python.exe")
    return 'Server shutting down...'
if __name__ == '__main__':
    app.run(debug=True)