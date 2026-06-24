# coding: utf-8
# license: GPLv3

"""Модуль расчёта модели движения космических объектов.

Для исходных файлов преподавателя оставлены функции расчёта гравитации.
Для финального экзаменационного варианта используется ООП-движение:
планеты и спутники сами обновляют своё положение методом update_position.
"""

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Эта функция оставлена для совместимости с исходным прототипом.
    """

    body.Fx = 0
    body.Fy = 0

    for obj in space_objects:
        if body == obj:
            continue

        dx = obj.x - body.x
        dy = obj.y - body.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared == 0:
            continue

        distance = distance_squared ** 0.5

        force = (
            gravitational_constant
            * body.m
            * obj.m
            / distance_squared
        )

        body.Fx += force * dx / distance
        body.Fy += force * dy / distance


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Эта функция оставлена для совместимости с исходным прототипом.
    """

    if body.m == 0:
        return

    ax = body.Fx / body.m
    ay = body.Fy / body.m

    body.x += body.Vx * dt + ax * dt ** 2 / 2
    body.y += body.Vy * dt + ay * dt ** 2 / 2

    body.Vx += ax * dt
    body.Vy += ay * dt


def use_orbit_model(space_objects):
    """Проверяет, есть ли в системе объекты с заданным центром вращения."""

    for body in space_objects:
        if getattr(body, "center", None) is not None:
            return True

    return False


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Если в системе есть планеты и спутники с центром вращения,
    используется ООП-модель кругового движения.
    Иначе используется старая физическая модель преподавателя.
    """

    if use_orbit_model(space_objects):
        for body in space_objects:
            body.update_position(dt)
        return

    for body in space_objects:
        calculate_force(body, space_objects)

    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")