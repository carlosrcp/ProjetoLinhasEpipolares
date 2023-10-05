import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import json

import numpy as np
import cv2

suffix = '_cin'

json_file_path = f"Pontos/points{suffix}.json"

try:
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
        points = data.get("points", [])
        print("JSON file found and loaded.")
except FileNotFoundError:
    points = []
    data = {"points": points}
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        print(f"JSON file '{json_file_path}' created with an empty list.")

json_file = open(json_file_path, "r")
data = json.load(json_file)
points = data.get("points", [])

current_point = -1
dsc_ponto = 'Novos Pontos'

def update_crosshair_position():
    x1 = x1_slider.get()
    y1 = y1_slider.get()
    x2 = x2_slider.get()
    y2 = y2_slider.get()

    canvas1.coords(crosshair1_top, x1-1, y1, x1-11, y1)
    canvas1.coords(crosshair1_bot, x1+2, y1, x1 + 12, y1)
    canvas1.coords(crosshair1_right, x1, y1+2, x1, y1 + 12)
    canvas1.coords(crosshair1_left, x1, y1-1, x1, y1-11)

    canvas2.coords(crosshair2_top, x2-1, y2, x2-11, y2)
    canvas2.coords(crosshair2_bot, x2+2, y2, x2 + 12, y2)
    canvas2.coords(crosshair2_right, x2, y2+2, x2, y2 + 12)
    canvas2.coords(crosshair2_left, x2, y2-1, x2, y2-11)

    global current_point
    
    if current_point >=0:
        points[current_point] = [[x1,y1],[x2,y2]]

window = tk.Tk()
window.title("Selecionar pontos correspondentes")

image1 = PhotoImage(file=f"Imagens/image1{suffix}.png")
image2 = PhotoImage(file=f"Imagens/image2{suffix}.png")

width = image1.width()
height = image1.height()
print(width)


label1 = tk.Label(window, image=image1)
label2 = tk.Label(window, image=image2)

x1_slider = tk.Scale(window, from_=0, to=width, length=width, orient="horizontal", label="X1")
y1_slider = tk.Scale(window, from_=0, to=height, length=width,orient="horizontal", label="Y1")
x2_slider = tk.Scale(window, from_=0, to=width, length=width,orient="horizontal", label="X2")
y2_slider = tk.Scale(window, from_=0, to=height, length=width,orient="horizontal", label="Y2")

x1_slider.set(width/2)
y1_slider.set(height/2)
x2_slider.set(width/2)
y2_slider.set(height/2)

def slider_updated(value):    
    update_crosshair_position()
x1_slider.config(command=lambda value: slider_updated(value))
y1_slider.config(command=lambda value: slider_updated(value))
y2_slider.config(command=lambda value: slider_updated(value))
x2_slider.config(command=lambda value: slider_updated(value))

canvas1 = tk.Canvas(window, width=width, height=height, bd=0, highlightthickness=0)
canvas2 = tk.Canvas(window, width=width, height=height, bd=0, highlightthickness=0)

canvas1.create_image(0,0,anchor=tk.NW, image=image1)
canvas2.create_image(0,0,anchor=tk.NW, image=image2)


crosshair1_top = canvas1.create_line(-1, 0, -11, 0, fill="red", width=3)
crosshair1_bot = canvas1.create_line(2, 0, 12, 0, fill="red", width=3)
crosshair1_right = canvas1.create_line(0, 2, 0, 12, fill="red", width=3)
crosshair1_left = canvas1.create_line(0, -11, 0, -1, fill="red", width=3)

crosshair2_top = canvas2.create_line(-1, 0, -11, 0, fill="red", width=3)
crosshair2_bot = canvas2.create_line(2, 0, 12, 0, fill="red", width=3)
crosshair2_right = canvas2.create_line(0, 2, 0, 12, fill="red", width=3)
crosshair2_left = canvas2.create_line(0, -11, 0, -1, fill="red", width=3)

update_crosshair_position()

def add_points():
    x1 = x1_slider.get()
    y1 = y1_slider.get()
    x2 = x2_slider.get()
    y2 = y2_slider.get()
    points.append([[x1,y1],[x2,y2]])

    print([[x1,y1],[x2,y2]])


text_label = tk.Label(window, text=dsc_ponto)
text_label.grid(row=0, column=0, columnspan=2)

def next_point():
    change_point(+1)

def prev_point():
    change_point(-1)


def change_point(i):
    global current_point
    current_point += i
    if current_point > len(points) - 1:
        current_point = -1
    if current_point < -1:
        current_point = len(points) - 1
    
    global dsc_ponto
    if current_point >=0:
        point1 = points[current_point][0]
        point2 = points[current_point][1]
        
        x1_slider.set(point1[0])
        y1_slider.set(point1[1])
        x2_slider.set(point2[0])
        y2_slider.set(point2[1])

        dsc_ponto = f'Par de pontos - {current_point}'
    else:
        global width
        global height
        x1_slider.set(width/2)
        y1_slider.set(height/2)
        x2_slider.set(width/2)
        y2_slider.set(height/2)

        dsc_ponto = f'Novo par de pontos'
    text_label.config(text=dsc_ponto)
    update_button.config(text=("Adicionar par de pontos" if current_point == -1 else "Atualizar par de pontos"))

def salvar():
    data = {"points": points}
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        print(f"JSON file '{json_file_path}' created with an empty list.")

def excluir():
    global current_point
    if current_point >= 0:
        points.pop(current_point)
    current_point -= 1
    change_point(0)


fun_matrix = None

lines1 = []
lines2 = []

update_button = tk.Button(window, text=("Adicionar par de pontos" if current_point == -1 else "Atualizar par de pontos"), command=add_points)
left_button = tk.Button(window, text="<", width=5, command=prev_point)
right_button = tk.Button(window, text=">", width=5, command=next_point)
save_button = tk.Button(window, text="Salvar", command=salvar)
delete_button = tk.Button(window, text="Excluir par de pontos", command=excluir)

label1.grid(row=0, column=0)
x1_slider.grid(row=1, column=0)
y1_slider.grid(row=2, column=0)
canvas1.grid(row=0, column=0)
label2.grid(row=0, column=1)
x2_slider.grid(row=1, column=1)
y2_slider.grid(row=2, column=1)
canvas2.grid(row=0, column=1)
text_label.grid(row=3, columnspan=2)
update_button.grid(row=4, columnspan=2)
left_button.grid(row=4, column=0)
right_button.grid(row=4, column=1)
delete_button.grid(row=5, columnspan=2)
save_button.grid(row=6, columnspan=2)

window.mainloop()