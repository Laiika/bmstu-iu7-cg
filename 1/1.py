from tkinter import Tk, Button, Label, Listbox, Canvas, messagebox, Entry, END, Listbox
from math import sqrt


TASK = 'На плоскости заданы два множества точек. Найти пару окружностей, каждая из которых проходит хотя бы через три различные точки \
одного и того же множества (окружности строятся на точках разных множеств) таких, что разность площадей четырехугольников, \
образованных центрами окружностей, точками касания внутренних общих касательных и точки пересечения касательных, максимальна. \
Сделать вывод в графическом режиме изображения'

CANVAS_W = 770
CANVAS_H = 720

EPS = 1e-10


class Point(object):
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return sqrt(dx * dx + dy * dy)


class Circle(object):
    def __init__(self, point1, point2, point3):
        self.points = [point1, point2, point3]
        # нахождение радиуса и центра окружности
        a = 2 * (point2.x - point1.x)
        b = 2 * (point2.y - point1.y)
        c = point2.x * point2.x - point1.x * point1.x + point2.y * point2.y - point1.y * point1.y
        d = 2 * (point3.x - point2.x)
        e = 2 * (point3.y - point2.y)
        f = point3.x * point3.x - point2.x * point2.x + point3.y * point3.y - point2.y * point2.y
        p = a * e - d * b
        x0 = (c * e - b * f) / p
        y0 = (a * f - c * d) / p
        self.center = Point(x0, y0, 0)
        self.r = self.center.distance(point1)



class Picture(object):
    def __init__(self, cl1, cl2, tng1, tng2, p_in):
        self.cl1 = cl1
        self.cl2 = cl2
        self.tng1 = tng1
        self.tng2 = tng2
        self.p_in = p_in


'''
    ВВОД
'''

# функция для создания окна ввода координат точки
def create_point_window():
    window = Tk()
    window.title("Ввод")
    window.geometry("270x200")

    x_label = Label(window, text="X: ")
    x_label.place(x=3, y=30)
    x = Entry(window)
    x.place(x=27, y=30)

    y_label = Label(window, text="Y: ")
    y_label.place(x=3, y=70)
    y = Entry(window)
    y.place(x=27, y=70)

    return window, x, y


# функция для обработки введенной точки в определенное множество
def process_point(tk_list, ps, ind, x, y):
    try:
        x = float(x)
        y = float(y)

        if ind != END:  # если нужно изменить точку
            tk_list.delete(ind)
            ps[ind].x = x
            ps[ind].y = y
            ps[ind].num = ind + 1
        else:  # если нужно добавить новую точку
            ind = len(ps)
            ps.append(Point(x, y, ind + 1))

        tk_list.insert(ind, "{:d}) {:.3f}, {:.3f}".format(ind + 1, x, y))
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")


# функция для удаления выделенной точки из определенного множества
def del_point(tk_list, ps):
    try:
        ind = tk_list.curselection()[0]
        ps.pop(ind)
        tk_list.delete(ind, END)

        for i in range(ind, len(ps)):
            ps[i].num = i + 1
            tk_list.insert(END, "{:d}) {:.3f}, {:.3f}".format(i + 1, ps[i].x, ps[i].y))
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для удаления")


# функция для удаления всех точек определенного множества
def del_all_points(tk_list, ps):
    if len(ps) != 0:
        tk_list.delete(0, END)
        ps.clear()
    else:
        messagebox.showerror("Ошибка", "И так пусто")


# функция для изменения выбранной точки из определенного множества
def change_point(tk_list, ps):
    try:
        ind = tk_list.curselection()[0]
        window, x, y = create_point_window()
        button = Button(window, text="Изменить", command=lambda: process_point(tk_list, ps, ind, x.get(), y.get()))
        button.place(x=70, y=120)

        window.mainloop()
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для изменения")


# функция для добавления точки в определенное множество
def add_point(tk_list, ps):
    window, x, y = create_point_window()

    button = Button(window, text="Добавить", command=lambda: process_point(tk_list, ps, END, x.get(), y.get()))
    button.place(x=70, y=120)

    window.mainloop()


'''
    РЕШЕНИЕ
'''

# функция для проверки, можно ли построить на трех точках окружность (не лежат ли они на одной прямой)
def check_circle(p1, p2, p3):
    pr1 = (p2.y - p1.y) * (p3.x - p1.x)
    pr2 = (p3.y - p1.y) * (p2.x - p1.x)

    if abs(pr1 - pr2) < EPS:
        return False

    return True


# функция для получения всех окружностей на заданном множестве
def get_circles(ps):
    cls = []
    n = len(ps)

    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if check_circle(ps[i], ps[j], ps[k]):
                    circle = Circle(ps[i], ps[j], ps[k])
                    cls.append(circle)

    return cls


# функция, возвращающая точки касания окружности
def get_kas_ps(cl, p):
    # параметры вспомогательной окружности
    xc2 = (p.x + cl.center.x) / 2
    yc2 = (p.y + cl.center.y) / 2
    pc2 = Point(xc2, yc2, 0)
    r2 = cl.center.distance(pc2)

    a = (cl.r * cl.r) / (2 * r2)
    h = sqrt(cl.r * cl.r - a * a)
    cos = (xc2 - cl.center.x) / r2
    sin = (yc2 - cl.center.y) / r2

    x = cl.center.x + a * cos
    y = cl.center.y + a * sin
    dy = h * cos
    dx = h * sin

    return Point(x + dx, y - dy, 0), Point(x - dx, y + dy, 0)


# функция для получения картины двух окружностей с внутренними касательными
def get_picture(cl1, cl2):
    # точка пересечения внутренних касательных
    d = cl1.r + cl2.r
    x_in = (cl1.r * cl2.center.x + cl2.r * cl1.center.x) / d
    y_in = (cl1.r * cl2.center.y + cl2.r * cl1.center.y) / d
    p_in = Point(x_in, y_in, 0)

    # точки касания первой окружности
    p1, p2 = get_kas_ps(cl1, p_in)
    # точки касания второй окружности
    p3, p4 = get_kas_ps(cl2, p_in)

    return Picture(cl1, cl2, [p1, p3], [p2, p4], p_in)


# функция для вычисления разности площадей
def get_dif_s(pic):
    p_in = pic.p_in
    p1 = pic.tng1[0]
    p2 = pic.tng1[1]

    s1 = pic.cl1.r * p1.distance(p_in)
    s2 = pic.cl2.r * p2.distance(p_in)

    return abs(s1 - s2)


# функция для решения задачи
def solve_task(ps1, ps2, canvas):
    canvas.delete('all')

    if len(ps1) < 3 or len(ps2) < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек")
        return

    cls1 = get_circles(ps1)
    cls2 = get_circles(ps2)

    if len(cls1) < 1 or len(cls2) < 1:
        messagebox.showerror("Ошибка", "Невозможно построить ни одну пару окружностей")
        return

    res_dif_s = -1
    res_pic = None

    for cl1 in cls1:
        for cl2 in cls2:
            if cl1.r + cl2.r < cl2.center.distance(cl1.center):
                pic = get_picture(cl1, cl2)
                dif_s = get_dif_s(pic)

                if dif_s > res_dif_s:
                    res_dif_s = dif_s
                    res_pic = pic

    if res_pic is None:
        messagebox.showerror("Ошибка", "Ни одна пара не имеет внутренних касательных")
        return

    print_result(res_pic, res_dif_s, canvas)


'''
    ВЫВОД
'''

# функция, вычисляющая координаты точки на холсте
def calc_coords(point, k, x_min, y_max):
    new_x = int(10 + k * (point.x - x_min))
    new_y = int(10 + k * (y_max - point.y))
    return new_x, new_y


# функция для вывода окружности и ее точек
def print_circle(cl, canvas, k, x_min, y_max, color):
    cl_x, cl_y = calc_coords(cl.center, k, x_min, y_max)
    cl_r = int(k * cl.r)
    canvas.create_oval(cl_x - cl_r, cl_y + cl_r, cl_x + cl_r, cl_y - cl_r, width=2, outline=color)

    for i in range(3):
        px, py = calc_coords(cl.points[i], k, x_min, y_max)
        canvas.create_text(px + 10, py - 10, text=f'{cl.points[i].num} ({cl.points[i].x}, {cl.points[i].y})')
        canvas.create_oval(px - 3, py + 3, px + 3, py - 3, fill='green')

    return cl_x, cl_y


# функция, выводящая результат
def print_result(pic, dif_s, canvas):
    xs = [pic.cl1.center.x + pic.cl1.r, pic.cl1.center.x - pic.cl1.r,
                   pic.cl2.center.x + pic.cl2.r, pic.cl2.center.x - pic.cl2.r]

    ys = [pic.cl1.center.y + pic.cl1.r, pic.cl1.center.y - pic.cl1.r,
                   pic.cl2.center.y + pic.cl2.r, pic.cl2.center.y - pic.cl2.r]

    x_max = max(xs)
    x_min = min(xs)
    y_max = max(ys)
    y_min = min(ys)

    k_x = (CANVAS_W * 0.8) / (x_max - x_min)
    k_y = (CANVAS_H * 0.8) / (y_max - y_min)

    k = min(k_x, k_y)

    cl1_x, cl1_y = print_circle(pic.cl1, canvas, k, x_min, y_max, 'red')
    cl2_x, cl2_y = print_circle(pic.cl2, canvas, k, x_min, y_max, 'blue')

    tng11_x, tng11_y = calc_coords(pic.tng1[0], k, x_min, y_max)
    tng12_x, tng12_y = calc_coords(pic.tng1[1], k, x_min, y_max)
    canvas.create_line(tng11_x, tng11_y, tng12_x, tng12_y, width=2)

    tng21_x, tng21_y = calc_coords(pic.tng2[0], k, x_min, y_max)
    tng22_x, tng22_y = calc_coords(pic.tng2[1], k, x_min, y_max)
    canvas.create_line(tng21_x, tng21_y, tng22_x, tng22_y, width=2)

    canvas.create_line(cl1_x, cl1_y, tng11_x, tng11_y, width=2)
    canvas.create_line(cl1_x, cl1_y, tng21_x, tng21_y, width=2)
    canvas.create_line(cl2_x, cl2_y, tng12_x, tng12_y, width=2)
    canvas.create_line(cl2_x, cl2_y, tng22_x, tng22_y, width=2)

    messagebox.showinfo(title='Ответ', message=f'Максимальная разность площадей четырехугольников равна {dif_s:.6}. \
Окружность первого множества - красная, второго - синяя.')


if __name__ == "__main__":
    points1 = []
    points2 = []

    window = Tk()
    window['bg'] = '#c7b446'
    window.geometry("1400x700")
    window.resizable(False, False)
    window.title("lr 1")

    canvas = Canvas(window, width=CANVAS_W, height=CANVAS_H)
    canvas.place(x=570, y=0)

    # первое множество
    label1 = Label(text="Первое множество точек")
    label1.place(x=10, y=10)

    list1 = Listbox(height=15, width=35)
    list1.place(x=10, y=50)

    add1 = Button(text="Добавить", width=10, height=3, command=lambda: add_point(list1, points1))
    add1.place(x=10, y=310)

    del1 = Button(text="Удалить", width=10, height=3, command=lambda: del_point(list1, points1))
    del1.place(x=10, y=370)

    ch1 = Button(text="Изменить", width=10, height=3, command=lambda: change_point(list1, points1))
    ch1.place(x=10, y=430)

    del_all1 = Button(text="Удалить все точки", width=20, height=3, command=lambda: del_all_points(list1, points1))
    del_all1.place(x=10, y=490)

    # второе множество
    label2 = Label(text="Второе множество точек")
    label2.place(x=270, y=10)

    list2 = Listbox(height=15, width=35)
    list2.place(x=270, y=50)

    add2 = Button(text="Добавить", width=10, height=3, command=lambda: add_point(list2, points2))
    add2.place(x=270, y=310)

    del2 = Button(text="Удалить", width=10, height=3, command=lambda: del_point(list2, points2))
    del2.place(x=270, y=370)

    ch2 = Button(text="Изменить", width=10, height=3, command=lambda: change_point(list2, points2))
    ch2.place(x=270, y=430)

    del_all2 = Button(text="Удалить все точки", width=20, height=3, command=lambda: del_all_points(list2, points2))
    del_all2.place(x=270, y=490)

    # про задачу
    task = Button(text="Вывести условие задачи", width=23, height=3, command=lambda: messagebox.showinfo("Задание", TASK))
    task.place(x=130, y=560)

    result = Button(text="Получить решение", width=23, height=3, command=lambda: solve_task(points1, points2, canvas))
    result.place(x=130, y=620)

    window.mainloop()
