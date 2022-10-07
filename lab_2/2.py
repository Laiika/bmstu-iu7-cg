from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from math import sqrt, atan, degrees, pi, sin, cos
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WIN_WIDTH = 1200
WIN_HEIGHT = 750
WIN_COLOR = '#c7b446'

CV_WIDE = 700
CV_HEIGHT = 700

GRAPH_WIDE = 60
GRAPH_HEIGHT = 60

# Прямоугольник
LEFT_RECT_X = -20
UP_RECT_Y = 9
RIGHT_RECT_X = 20
DOWN_RECT_Y = -9

# Окружность
RADIUS = 4

X_CENTER = 0
Y_CENTER = 0


# Функция для нахождения координат вершин прямоугольника
def init_rectangle():
    x_left = LEFT_RECT_X + X_CENTER
    x_right = RIGHT_RECT_X + X_CENTER
    y_up = UP_RECT_Y + Y_CENTER
    y_down = DOWN_RECT_Y + Y_CENTER

    x_rect = [x_left, x_right, x_right, x_left, x_left]
    y_rect = [y_down, y_down, y_up, y_up, y_down]

    return x_rect, y_rect


# Функция для отрисовки прямоугольника
def draw_rectangle(x_rect, y_rect):
    plt.plot(x_rect, y_rect, linewidth=2)


# Функция для нахождения координат вершин ромба
def init_rhomb():
    x_left = LEFT_RECT_X + X_CENTER

    x_rhomb = [x_left, X_CENTER, RIGHT_RECT_X + X_CENTER, X_CENTER, x_left]
    y_rhomb = [Y_CENTER, UP_RECT_Y + Y_CENTER, Y_CENTER, DOWN_RECT_Y + Y_CENTER, Y_CENTER]

    return x_rhomb, y_rhomb


# Функция для отрисовки ромба
def draw_rhomb(x_rhomb, y_rhomb):
    plt.plot(x_rhomb, y_rhomb, linewidth=2)


# Функция для нахождения координат окружности
def init_circle():
    angle = np.linspace(0, 2 * np.pi, 150)

    x_circle = RADIUS * np.cos(angle)
    y_circle = RADIUS * np.sin(angle)

    return x_circle, y_circle


# Функция для отрисовки окружности
def draw_circle(x_circle, y_circle):
    plt.plot(x_circle, y_circle, linewidth=2)


# Функция для нахождения координат вершин плюса
def init_plus():
    x_plus = [X_CENTER - RADIUS, X_CENTER, RADIUS + X_CENTER, X_CENTER]
    y_plus = [Y_CENTER, RADIUS + Y_CENTER, Y_CENTER, Y_CENTER - RADIUS]

    return x_plus, y_plus


# Функция для отрисовки плюса
def draw_plus(x_plus, y_plus):
    plt.plot([x_plus[0], x_plus[2]], [y_plus[0], y_plus[2]], linewidth=2)
    plt.plot([x_plus[1], x_plus[3]], [y_plus[1], y_plus[3]], linewidth=2)


# Функция для нахождения координат правой дуги
def init_right_arc():
    xc = RIGHT_RECT_X // 2
    tg = UP_RECT_Y / xc
    angle = np.linspace(atan(tg), -atan(tg), 75)

    r = sqrt(xc * xc + UP_RECT_Y * UP_RECT_Y)
    x_arc = r * np.cos(angle) + xc
    y_arc = r * np.sin(angle)

    return x_arc, y_arc


# Функция для отрисовки правой дуги
def draw_right_arc(x_arc, y_arc):
    plt.plot(x_arc, y_arc, linewidth=2)


# Функция для нахождения координат левой дуги
def init_left_arc():
    xc = RIGHT_RECT_X // 2
    tg = UP_RECT_Y / xc
    angle = np.linspace(np.pi - atan(tg), np.pi + atan(tg), 75)

    r = sqrt(xc * xc + UP_RECT_Y * UP_RECT_Y)
    x_arc = r * np.cos(angle) - xc
    y_arc = r * np.sin(angle)

    return x_arc, y_arc


# Функция для отрисовки левой дуги
def draw_left_arc(x_arc, y_arc):
    plt.plot(x_arc, y_arc, linewidth=2)


# Функция для отрисовки всей картины
def draw_picrure(x_all, y_all):
    build_empty_figure()

    draw_rectangle(x_all[1], y_all[1])
    draw_rhomb(x_all[2], y_all[2])
    draw_circle(x_all[3], y_all[3])
    draw_plus(x_all[4], y_all[4])
    draw_right_arc(x_all[5], y_all[5])
    draw_left_arc(x_all[6], y_all[6])
    canvas.draw()


# Функция для вычисления координат всех необходимых объектов
def init_all():
    x_rect, y_rect = init_rectangle()
    x_rhomb, y_rhomb = init_rhomb()
    x_circle, y_circle = init_circle()
    x_plus, y_plus = init_plus()
    x_arcr, y_arcr = init_right_arc()
    x_arcl, y_arcl = init_left_arc()

    x_all = [[X_CENTER], x_rect, x_rhomb, x_circle, x_plus, x_arcr, x_arcl]
    y_all = [[Y_CENTER], y_rect, y_rhomb, y_circle, y_plus, y_arcr, y_arcl]

    draw_picrure(x_all, y_all)

    return x_all, y_all


# Функция для вычисления координат всех нужных точек при перемещении
def move(x_all, y_all, dx, dy):
    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] += dx
            y_all[i][j] += dy

    set_figure_center(x_all[0][0], y_all[0][0])

    global x_history, y_history

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


# Функция для вычисления координат всех нужных точек при повороте
def spin(x_all, y_all, angle, x_c, y_c):
    angle = (angle * pi) / 180

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] -= x_c
            y_all[i][j] -= y_c
            x_copy = x_all[i][j]
            y_copy = y_all[i][j]

            x_all[i][j] = x_c + x_copy * cos(angle) - y_copy * sin(angle)
            y_all[i][j] = x_c + x_copy * sin(angle) + y_copy * cos(angle)

    set_figure_center(x_all[0][0], y_all[0][0])

    global x_history, y_history

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


# Функция для вычисления координат всех нужных точек при масштабировании
def scale(x_all, y_all, x_c, y_c, kx, ky):
    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] = kx * (x_all[i][j] - x_c) + x_c
            y_all[i][j] = ky * (y_all[i][j] - y_c) + y_c

    set_figure_center(x_all[0][0], y_all[0][0])

    global x_history, y_history

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


# Функция для очистки поля для последующего построения на нем фигуры
def build_empty_figure():
    global ax

    fig.clear()

    ax = fig.add_subplot(111)

    ax.set_xlim([-GRAPH_WIDE, GRAPH_WIDE])
    ax.set_ylim([-GRAPH_HEIGHT, GRAPH_HEIGHT])
    ax.grid()

    fig.subplots_adjust(right=0.97, left=0.06, bottom=0.06, top=0.97)

    canvas.draw()


# Функция для сброса всех преобразований и возврата к начальному состояни фигуры
def reset():
    global x_all, y_all, x_history, y_history

    if (len(x_history) == 1):
        messagebox.showerror("Стоп", "Вы дошли до начального изображения")
        return

    set_figure_center(0, 0)

    x_all, y_all = init_all()

    x_history.clear()
    y_history.clear()

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))


# Функция для возврата к предыдущему состоянию фигуры
def step_backing():
    global x_history, y_history

    if (len(x_history) == 1):
        messagebox.showerror("Стоп", "Вы дошли до начального изображения")
        return

    x_history.pop()
    y_history.pop()

    x_len = len(x_history)
    y_len = len(y_history)
    set_figure_center(x_history[x_len - 1][0][0], y_history[y_len - 1][0][0])
    draw_picrure(x_history[x_len - 1], y_history[y_len - 1])


# Функция для отрисовки в приложении текущего центра фигуры
def set_figure_center(x_c, y_c):
    figure_c = Label(win, text="Центр фигуры: (%3.2f;%3.2f)" % (x_c, y_c), width=32, font="-family {Consolas} -size 17")
    figure_c.place(x=CV_WIDE + 45, y=660)


# Функция обработки параметров для перемещения и вызова функции перемещения
def parse_move():
    try:
        dx = float(move_x.get())
        dy = float(move_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введена величина смещения (надо вводить числа)")
        return

    global x_history, y_history

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    move(x_cur, y_cur, dx, dy)


# Функция обработки параметров для поворота и вызова функции поворота
def parse_spin():
    try:
        x_c = float(center_x.get())
        y_c = float(center_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота (надо вводить числа)")
        return

    try:
        angle = float(spin_angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введен угол поворота (надо вводить числа)")
        return

    global x_history, y_history

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    spin(x_cur, y_cur, angle, x_c, y_c)


# Функция обработки параметров для масштабирования и вызова функции масштабирования
def parse_scale():
    try:
        x_c = float(center_x.get())
        y_c = float(center_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота (надо вводить числа)")
        return

    try:
        kx = float(scale_x.get())
        ky = float(scale_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены коэффициенты масштабирования (надо вводить числа)")
        return

    global x_history, y_history

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    scale(x_cur, y_cur, x_c, y_c, kx, ky)


if __name__ == "__main__":
    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" % (WIN_WIDTH, WIN_HEIGHT))
    win.title("LR 2")
    win.resizable(False, False)

    x_history = []
    y_history = []

    fig = plt.figure()

    canvas = FigureCanvasTkAgg(fig, master=win)
    plot = canvas.get_tk_widget()
    plot.place(x=0, y=0, width=CV_WIDE, height=CV_HEIGHT)
    build_empty_figure()

    x_all, y_all = init_all()

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    canvas.draw()

    # Центр фигуры
    figure_c = Label(win, text="Центр фигуры: (%3.2f;%3.2f)" % (x_all[0][0], y_all[0][0]), width=36,
                     font="-family {Consolas} -size 15")
    figure_c.place(x=CV_WIDE + 45, y=660)

    # Центр для масштабирования и поворота
    center_label = Label(win, text="Центр для масштабирования и поворота", font="-family {Consolas} -size 15", bg=WIN_COLOR)
    center_label.place(x=CV_WIDE + 45, y=20)

    center_x_label = Label(win, text="X:", font="-family {Consolas} -size 14", bg=WIN_COLOR)
    center_x_label.place(x=CV_WIDE + 70, y=50)
    center_x = Entry(win, font="-family {Consolas} -size 14", width=9)
    center_x.insert(END, "0")
    center_x.place(x=CV_WIDE + 100, y=50)

    center_y_label = Label(win, text="Y:", font="-family {Consolas} -size 14", bg=WIN_COLOR)
    center_y_label.place(x=CV_WIDE + 270, y=50)
    center_y = Entry(win, font="-family {Consolas} -size 14", width=9)
    center_y.insert(END, "0")
    center_y.place(x=CV_WIDE + 300, y=50)

    # Поворот
    spin_label = Label(win, text="Поворот", width=36, font="-family {Consolas} -size 16")
    spin_label.place(x=CV_WIDE + 1, y=90)

    spin_angle_label = Label(win, text="Угол: ", font="-family {Consolas} -size 15", bg=WIN_COLOR)
    spin_angle_label.place(x=CV_WIDE + 160, y=135)
    spin_angle = Entry(win, font="-family {Consolas} -size 16", width=9)
    spin_angle.insert(END, "0")
    spin_angle.place(x=CV_WIDE + 240, y=135)

    spin_btn = Button(win, text="Повернуть", font="-family {Consolas} -size 14", command=lambda: parse_spin(), width=15, height=1)
    spin_btn.place(x=CV_WIDE + 160, y=180)

    # Масштабирование
    scale_label = Label(win, text="Масштабирование", width=36, font="-family {Consolas} -size 16")
    scale_label.place(x=CV_WIDE + 1, y=240)

    scale_x_label = Label(win, text="kx: ", font="-family {Consolas} -size 15", bg=WIN_COLOR)
    scale_x_label.place(x=CV_WIDE + 100, y=300)
    scale_x = Entry(win, font="-family {Consolas} -size 14", width=9)
    scale_x.insert(END, "1")
    scale_x.place(x=CV_WIDE + 140, y=300)

    scale_y_label = Label(win, text="ky: ", font="-family {Consolas} -size 16", bg=WIN_COLOR)
    scale_y_label.place(x=CV_WIDE + 270, y=300)
    scale_y = Entry(win, font="-family {Consolas} -size 14", width=9)
    scale_y.insert(END, "1")
    scale_y.place(x=CV_WIDE + 310, y=300)

    scale_btn = Button(win, text="Масштабировать", font="-family {Consolas} -size 14", command=lambda: parse_scale(), width=15,
                       height=1)
    scale_btn.place(x=CV_WIDE + 160, y=350)

    # Перемещение
    move_label = Label(win, text="Перенос", width=36, font="-family {Consolas} -size 16")
    move_label.place(x=CV_WIDE + 1, y=410)

    move_x_label = Label(win, text="dx: ", font="-family {Consolas} -size 15", bg=WIN_COLOR)
    move_x_label.place(x=CV_WIDE + 100, y=460)
    move_x = Entry(win, font="-family {Consolas} -size 14", width=9)
    move_x.insert(END, "0")
    move_x.place(x=CV_WIDE + 140, y=460)

    move_y_label = Label(win, text="dy: ", font="-family {Consolas} -size 16", bg=WIN_COLOR)
    move_y_label.place(x=CV_WIDE + 270, y=460)
    move_y = Entry(win, font="-family {Consolas} -size 14", width=9)
    move_y.insert(END, "0")
    move_y.place(x=CV_WIDE + 310, y=460)

    move_btn = Button(win, text="Перенести", font="-family {Consolas} -size 14", command=lambda: parse_move(), width=15,
                      height=1)
    move_btn.place(x=CV_WIDE + 160, y=500)

    line = Label(win, text="", width=36, font="-family {Consolas} -size 18")
    line.place(x=CV_WIDE + 1, y=550)

    # Возвращение
    stab_back = Button(win, text="Шаг назад", font="-family {Consolas} -size 14", command=lambda: step_backing(), width=15,
                       height=1)
    stab_back.place(x=CV_WIDE + 25, y=600)

    clear = Button(win, text="Сбросить", font="-family {Consolas} -size 14", command=lambda: reset(), width=15, height=1)
    clear.place(x=CV_WIDE + 300, y=600)

    win.mainloop()