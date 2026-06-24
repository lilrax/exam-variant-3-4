# coding: utf-8
# license: GPLv3

"""Модуль чтения и записи данных о космических объектах."""

from solar_objects import Planet, Satellite, Star


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла.

    Поддерживает старый формат преподавателя:
    Star <радиус> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус> <цвет> <масса> <x> <y> <Vx> <Vy>
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
    """Считывает данные о звезде из строки."""

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
    """Считывает данные о планете из строки."""

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


def get_object_type_for_file(obj):
    """Возвращает название типа объекта для записи в файл."""

    if isinstance(obj, Star) or obj.type == "star":
        return "Star"

    if isinstance(obj, Planet) or obj.type == "planet":
        return "Planet"

    if isinstance(obj, Satellite) or obj.type == "satellite":
        return "Satellite"

    return "Unknown"


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Для совместимости сохраняются основные параметры:
    тип, радиус, цвет, масса, координаты и скорость.
    """

    with open(output_filename, "w", encoding="utf-8") as out_file:
        print("# Saved solar system state", file=out_file)

        for obj in space_objects:
            object_type = get_object_type_for_file(obj)

            if object_type == "Unknown":
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