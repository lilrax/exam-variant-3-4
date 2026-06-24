# coding: utf-8
# license: GPLv3

"""Модуль чтения и записи данных о космических объектах."""

from solar_objects import Planet, Star


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла.

    Создаёт объекты Star и Planet и заполняет их параметры.

    Параметры:

    **input_filename** — имя входного файла.
    """

    objects = []

    with open(input_filename, encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            object_type = line.split()[0].lower()

            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object:", object_type)

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты звезды, (Vx, Vy) — скорость.

    Параметры:

    **line** — строка с описанием звезды.
    **star** — объект звезды.
    """

    parts = line.split()

    if len(parts) != 8:
        raise ValueError("Неверный формат строки звезды: " + line)

    star.R = int(float(parts[1]))
    star.color = parts[2]
    star.m = float(parts[3])
    star.x = float(parts[4])
    star.y = float(parts[5])
    star.Vx = float(parts[6])
    star.Vy = float(parts[7])


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.

    Входная строка должна иметь следующий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Параметры:

    **line** — строка с описанием планеты.
    **planet** — объект планеты.
    """

    parts = line.split()

    if len(parts) != 8:
        raise ValueError("Неверный формат строки планеты: " + line)

    planet.R = int(float(parts[1]))
    planet.color = parts[2]
    planet.m = float(parts[3])
    planet.x = float(parts[4])
    planet.y = float(parts[5])
    planet.Vx = float(parts[6])
    planet.Vy = float(parts[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки имеют следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя выходного файла.
    **space_objects** — список объектов планет и звёзд.
    """

    with open(output_filename, "w", encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == "star":
                object_type = "Star"
            elif obj.type == "planet":
                object_type = "Planet"
            else:
                continue

            line = (
                f"{object_type} "
                f"{obj.R} "
                f"{obj.color} "
                f"{obj.m:.6E} "
                f"{obj.x:.6E} "
                f"{obj.y:.6E} "
                f"{obj.Vx:.6E} "
                f"{obj.Vy:.6E}"
            )

            print(line, file=out_file)


if __name__ == "__main__":
    print("This module is not for direct call!")
