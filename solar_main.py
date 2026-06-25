# coding: utf-8
# license: GPLv3

"""Главный модуль программы."""

import tkinter
from math import pi
from tkinter.filedialog import askopenfilename, asksaveasfilename

from solar_input import read_space_objects_data_from_file
from solar_input import write_space_objects_data_to_file
from solar_model import recalculate_space_objects_positions
from solar_objects import Planet, Satellite, Star
from solar_vis import calculate_scale_factor
from solar_vis import create_orbit_image
from solar_vis import create_planet_image
from solar_vis import create_satellite_image
from solar_vis import create_star_image
from solar_vis import set_orbit_visibility
from solar_vis import update_object_position
from solar_vis import update_system_name
from solar_vis import window_height
from solar_vis import window_width

perform_execution = False
physical_time = 0
displayed_time = None
time_step = None
time_speed = None
space = None
start_button = None
orbit_button = None
show_orbits = True
space_objects = []


def get_max_distance(objects):
    """Возвращает максимальное расстояние объекта от центра экрана."""

    if not objects:
        return 1

    max_distance = 1

    for obj in objects:
        object_distance = max(abs(obj.x), abs(obj.y))
        orbit_radius = getattr(obj, "orbit_radius", 0)
        max_distance = max(max_distance, object_distance + orbit_radius)

    return max_distance


def add_satellites_to_planet(planet, count, star_index, planet_number):
    """Создаёт спутники для выбранной планеты."""

    satellites = []

    for satellite_index in range(count):
        angle = 2 * pi * satellite_index / count
        direction = 1 if satellite_index % 2 == 0 else -1

        satellite = Satellite(
            radius=2,
            color="white",
            mass=1.0E20,
            center=planet,
            orbit_radius=16 + 4 * satellite_index,
            angle=angle,
            angular_speed=0.035 + 0.004 * satellite_index,
            direction=direction,
            name=(
                f"Satellite "
                f"{star_index + 1}."
                f"{planet_number}."
                f"{satellite_index + 1}"
            ),
        )

        planet.add_satellite(satellite)
        satellites.append(satellite)

    return satellites


def get_satellite_count(star_index, planet_number):
    """Возвращает количество спутников для планеты по билету №5.

    В билете указано, что у 5, 10, 20, 30, 40, 50 планеты первой звезды
    должно быть по одному спутнику. У первой звезды по условию всего
    20 планет, поэтому реально создаются спутники у 5, 10 и 20 планеты.
    """

    satellite_count = 0

    if star_index == 0 and planet_number in (5, 10, 20):
        satellite_count += 1

    if star_index in (1, 3) and planet_number in (10, 20):
        satellite_count += 3

    if star_index in (1, 3) and planet_number in (5, 10, 15):
        satellite_count += 5

    return satellite_count


def build_exam_variant_system():
    """Создаёт систему по варианту 3–4 / билету №5.

    Требования варианта:
    - 5 звёзд;
    - 20, 30, 30, 20, 15 планет;
    - планеты могут находиться по нескольку на одной орбите;
    - у части планет есть спутники;
    - орбиты разных звёзд пересекаются;
    - направление вращения различается.
    """

    objects = []

    star_positions = [
        (-420, -170),
        (0, -210),
        (420, -170),
        (-230, 210),
        (230, 210),
    ]

    star_colors = ["yellow", "cyan", "orange", "red", "white"]
    planets_per_star = [20, 30, 30, 20, 15]
    max_planets_on_orbit = [5, 4, 3, 4, 3]

    planet_colors = [
        "green",
        "blue",
        "gray",
        "orange",
        "pink",
        "lightblue",
        "violet",
        "brown",
    ]

    for star_index in range(5):
        star = Star(
            radius=14,
            color=star_colors[star_index],
            mass=1.0E30,
            x=star_positions[star_index][0],
            y=star_positions[star_index][1],
            name=f"Star {star_index + 1}",
        )

        objects.append(star)

        planet_count = planets_per_star[star_index]
        max_on_orbit = max_planets_on_orbit[star_index]

        for planet_index in range(planet_count):
            planet_number = planet_index + 1
            orbit_level = planet_index // max_on_orbit
            place_on_orbit = planet_index % max_on_orbit

            orbit_radius = 45 + orbit_level * 26 + star_index * 4
            angle = 2 * pi * place_on_orbit / max_on_orbit

            direction = 1
            if (planet_index + star_index) % 2 == 1:
                direction = -1

            planet = Planet(
                radius=3 + planet_index % 3,
                color=planet_colors[planet_index % len(planet_colors)],
                mass=1.0E24,
                center=star,
                orbit_radius=orbit_radius,
                angle=angle,
                angular_speed=0.010 + 0.0007 * orbit_level,
                direction=direction,
                name=f"Planet {star_index + 1}.{planet_number}",
            )

            star.add_planet(planet)
            objects.append(planet)

            satellite_count = get_satellite_count(star_index, planet_number)
            objects.extend(
                add_satellites_to_planet(
                    planet,
                    satellite_count,
                    star_index,
                    planet_number,
                )
            )

    return objects


def execution():
    """Циклически пересчитывает и обновляет положение объектов."""

    global physical_time

    recalculate_space_objects_positions(space_objects, time_step.get())

    for body in space_objects:
        update_object_position(space, body)

    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        delay = max(1, 101 - int(time_speed.get()))
        space.after(delay, execution)


def start_execution():
    """Запускает моделирование."""

    global perform_execution

    if perform_execution:
        return

    perform_execution = True
    start_button["text"] = "Pause"
    start_button["command"] = stop_execution

    execution()
    print("Started execution...")


def stop_execution():
    """Останавливает моделирование."""

    global perform_execution

    perform_execution = False
    start_button["text"] = "Start"
    start_button["command"] = start_execution
    print("Paused execution.")


def toggle_execution(event=None):
    """Запускает или останавливает моделирование по клавише Пробел."""

    if perform_execution:
        stop_execution()
    else:
        start_execution()


def toggle_orbits():
    """Включает и выключает отображение орбит."""

    global show_orbits

    show_orbits = not show_orbits

    for body in space_objects:
        set_orbit_visibility(space, body, show_orbits)

    if show_orbits:
        orbit_button["text"] = "Hide orbits"
    else:
        orbit_button["text"] = "Show orbits"


def clear_space():
    """Очищает холст от старых изображений."""

    for obj in space_objects:
        if getattr(obj, "image", None) is not None:
            space.delete(obj.image)

        if getattr(obj, "orbit_image", None) is not None:
            space.delete(obj.orbit_image)

    space.delete("header")


def create_images_for_objects():
    """Создаёт изображения всех объектов системы."""

    for obj in space_objects:
        if obj.type in ("planet", "satellite"):
            create_orbit_image(space, obj)
            set_orbit_visibility(space, obj, show_orbits)

    for obj in space_objects:
        if obj.type == "star":
            create_star_image(space, obj)
        elif obj.type == "planet":
            create_planet_image(space, obj)
        elif obj.type == "satellite":
            create_satellite_image(space, obj)
        else:
            raise AssertionError("Unknown object type")

    update_system_name(
        space,
        "Exam variant 3-4: 5 stars, 115 planets, satellites",
    )


def load_exam_variant():
    """Загружает систему по варианту 3–4."""

    global space_objects
    global physical_time
    global perform_execution

    perform_execution = False
    physical_time = 0
    displayed_time.set(str(physical_time) + " seconds gone")

    clear_space()

    space_objects = build_exam_variant_system()

    calculate_scale_factor(get_max_distance(space_objects))
    create_images_for_objects()

    start_button["text"] = "Start"
    start_button["command"] = start_execution

    print("Exam variant 3-4 loaded")
    print("Objects:", len(space_objects))


def open_file_dialog():
    """Открывает систему из файла преподавателя."""

    global space_objects
    global physical_time
    global perform_execution

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

    calculate_scale_factor(get_max_distance(space_objects))
    create_images_for_objects()

    start_button["text"] = "Start"
    start_button["command"] = start_execution


def save_file_dialog():
    """Сохраняет текущее состояние системы в файл."""

    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))

    if not out_filename:
        return

    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция программы."""

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
    root.title("Solar system — exam variant 3-4")
    root.geometry("1100x680")
    root.minsize(900, 620)

    main_frame = tkinter.Frame(root)
    main_frame.pack(fill=tkinter.BOTH, expand=True)

    space = tkinter.Canvas(
        main_frame,
        width=window_width,
        height=window_height,
        bg="black",
    )
    space.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    frame = tkinter.Frame(main_frame)
    frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    start_button = tkinter.Button(
        frame,
        text="Start",
        command=start_execution,
        width=8,
    )
    start_button.pack(side=tkinter.LEFT, padx=2, pady=4)

    orbit_button = tkinter.Button(
        frame,
        text="Hide orbits",
        command=toggle_orbits,
        width=10,
    )
    orbit_button.pack(side=tkinter.LEFT, padx=2, pady=4)

    load_variant_button = tkinter.Button(
        frame,
        text="Load variant 3-4",
        command=load_exam_variant,
        width=15,
    )
    load_variant_button.pack(side=tkinter.LEFT, padx=2, pady=4)

    time_step = tkinter.DoubleVar()
    time_step.set(1)

    time_step_entry = tkinter.Entry(frame, textvariable=time_step, width=8)
    time_step_entry.pack(side=tkinter.LEFT, padx=2, pady=4)

    time_speed = tkinter.DoubleVar()
    time_speed.set(50)

    scale = tkinter.Scale(
        frame,
        variable=time_speed,
        orient=tkinter.HORIZONTAL,
        length=150,
    )
    scale.pack(side=tkinter.LEFT, padx=2, pady=0)

    load_file_button = tkinter.Button(
        frame,
        text="Open file...",
        command=open_file_dialog,
    )
    load_file_button.pack(side=tkinter.LEFT, padx=2, pady=4)

    save_file_button = tkinter.Button(
        frame,
        text="Save to file...",
        command=save_file_dialog,
    )
    save_file_button.pack(side=tkinter.LEFT, padx=2, pady=4)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")

    time_label = tkinter.Label(
        frame,
        textvariable=displayed_time,
        width=24,
    )
    time_label.pack(side=tkinter.RIGHT, padx=2, pady=4)

    root.bind("<space>", toggle_execution)

    load_exam_variant()

    root.mainloop()
    print("Modelling finished!")


if __name__ == "__main__":
    main()