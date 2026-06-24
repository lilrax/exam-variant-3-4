# coding: utf-8
# license: GPLv3

"""Модуль расчёта физической модели движения космических объектов."""

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Сила считается по закону всемирного тяготения Ньютона.
    На тело body действуют все остальные объекты из списка space_objects.

    Параметры:

    **body** — тело, для которого нужно вычислить действующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
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

    Используется простая численная схема:
    сначала вычисляется ускорение, затем обновляются координаты и скорость.

    Параметры:

    **body** — тело, которое нужно переместить.
    **dt** — шаг по времени.
    """

    if body.m == 0:
        return

    ax = body.Fx / body.m
    ay = body.Fy / body.m

    body.x += body.Vx * dt + ax * dt ** 2 / 2
    body.y += body.Vy * dt + ay * dt ** 2 / 2

    body.Vx += ax * dt
    body.Vy += ay * dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени.
    """

    for body in space_objects:
        calculate_force(body, space_objects)

    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
