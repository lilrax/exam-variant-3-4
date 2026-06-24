# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *

from solar_input import *
from solar_model import *
from solar_vis import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

time_speed = None
"""Скорость отображения моделирования.
Тип: переменная tkinter"""

space = None
"""Холст для отображения объектов."""

start_button = None
"""Кнопка запуска и остановки моделирования."""

orbit_button = None
"""Кнопка включения и выключения отображения орбит."""

show_orbits = True
"""Флаг отображения орбит."""

space_objects = []
"""Список космических объектов."""


def execution():
    """Функция исполнения.

    Выполняется циклически, вызывает обработку всех небесных тел,
    а также обновляет их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной
    perform_execution.
    """

    global physical_time
    global displayed_time

    recalculate_space_objects_positions(space_objects, time_step.get())

    for body in space_objects:
        update_object_position(space, body)

    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.

    Запускает циклическое исполнение функции execution.
    """

    global perform_execution

    perform_execution = True
    start_button["text"] = "Pause"
    start_button["command"] = stop_execution

    execution()
    print("Started execution...")


def stop_execution():
    """Обработчик события нажатия на кнопку Pause.

    Останавливает циклическое исполнение функции execution.
    """

    global perform_execution

    perform_execution = False
    start_button["text"] = "Start"
    start_button["command"] = start_execution
    print("Paused execution.")


def toggle_orbits():
    """Включает и выключает отображение орбит в интерфейсе программы."""

    global show_orbits

    show_orbits = not show_orbits

    for body in space_objects:
        set_orbit_visibility(space, body, show_orbits)

    if show_orbits:
        orbit_button["text"] = "Hide orbits"
    else:
        orbit_button["text"] = "Show orbits"


def clear_space():
    """Удаляет старые изображения объектов и орбит с холста."""

    for obj in space_objects:
        if getattr(obj, "image", None) is not None:
            space.delete(obj.image)

        if getattr(obj, "orbit_image", None) is not None:
            space.delete(obj.orbit_image)


def create_images_for_objects():
    """Создаёт изображения звёзд, планет и орбит."""

    for obj in space_objects:
        if obj.type == "star":
            create_star_image(space, obj)
        elif obj.type == "planet":
            create_orbit_image(space, obj)
            set_orbit_visibility(space, obj, show_orbits)
            create_planet_image(space, obj)
        else:
            raise AssertionError("Unknown object type")


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла.

    После выбора файла считывает параметры системы небесных тел.
    Считанные объекты сохраняются в глобальный список space_objects.
    """

    global space_objects
    global perform_execution
    global physical_time

    perform_execution = False
    physical_time = 0
    displayed_time.set(str(physical_time) + " seconds gone")

    clear_space()

    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if not in_filename:
        return

    space_objects = read_space_objects_data_from_file(in_filename)

    if not space_objects:
        return

    max_distance = max(
        [max(abs(obj.x), abs(obj.y)) for obj in space_objects]
    )

    if max_distance == 0:
        max_distance = 1

    calculate_scale_factor(max_distance)
    create_images_for_objects()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла.

    Вызывает функцию записи текущего состояния системы в файл.
    """

    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if not out_filename:
        return

    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.

    Создаёт объекты графического интерфейса tkinter:
    окно, холст, фрейм с кнопками, кнопки, поля ввода.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global orbit_button

    print("Modelling started!")
    physical_time = 0

    root = tkinter.Tk()
    root.title("Solar system")

    space = tkinter.Canvas(
        root,
        width=window_width,
        height=window_height,
        bg="black"
    )
    space.pack(side=tkinter.TOP)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(
        frame,
        text="Start",
        command=start_execution,
        width=8
    )
    start_button.pack(side=tkinter.LEFT)

    orbit_button = tkinter.Button(
        frame,
        text="Hide orbits",
        command=toggle_orbits,
        width=10
    )
    orbit_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)

    time_step_entry = tkinter.Entry(frame, textvariable=time_step, width=8)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    time_speed.set(50)

    scale = tkinter.Scale(
        frame,
        variable=time_speed,
        orient=tkinter.HORIZONTAL
    )
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(
        frame,
        text="Open file...",
        command=open_file_dialog
    )
    load_file_button.pack(side=tkinter.LEFT)

    save_file_button = tkinter.Button(
        frame,
        text="Save to file...",
        command=save_file_dialog
    )
    save_file_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")

    time_label = tkinter.Label(
        frame,
        textvariable=displayed_time,
        width=30
    )
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print("Modelling finished!")


if __name__ == "__main__":
    main()