# coding: utf-8
# license: GPLv3

"""Модуль визуализации.

Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране,
принимают физические координаты.
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 1000
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = None
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр.
"""


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине."""

    global scale_factor

    if max_distance == 0:
        max_distance = 1

    scale_factor = 0.45 * min(window_height, window_width) / max_distance
    print("Scale factor:", scale_factor)


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели."""

    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.

    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.
    """

    return window_height // 2 - int(y * scale_factor)


def create_circle_image(space, body):
    """Создаёт круглый графический объект для звезды, планеты или спутника."""

    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R

    body.image = space.create_oval(
        [x - r, y - r],
        [x + r, y + r],
        fill=body.color,
        outline=body.color
    )


def create_star_image(space, star):
    """Создаёт отображаемый объект звезды."""

    create_circle_image(space, star)


def create_planet_image(space, planet):
    """Создаёт отображаемый объект планеты."""

    create_circle_image(space, planet)


def create_satellite_image(space, satellite):
    """Создаёт отображаемый объект спутника."""

    create_circle_image(space, satellite)


def create_orbit_image(space, body):
    """Создаёт изображение орбиты для объекта.

    Для планеты орбита строится вокруг звезды.
    Для спутника орбита строится вокруг планеты.
    """

    center = getattr(body, "center", None)
    orbit_radius = getattr(body, "orbit_radius", None)

    if center is None or orbit_radius is None:
        return

    center_x = scale_x(center.x)
    center_y = scale_y(center.y)
    radius = int(orbit_radius * scale_factor)

    body.orbit_image = space.create_oval(
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius,
        outline="gray25"
    )


def set_orbit_visibility(space, body, visible):
    """Включает или выключает отображение орбиты объекта."""

    orbit_image = getattr(body, "orbit_image", None)

    if orbit_image is None:
        return

    state = "normal" if visible else "hidden"
    space.itemconfigure(orbit_image, state=state)


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел."""

    space.delete("header")
    space.create_text(
        20,
        25,
        tag="header",
        text=system_name,
        font=header_font,
        fill="white",
        anchor="w"
    )


def update_object_position(space, body):
    """Перемещает отображаемый объект на холсте."""

    if body.image is None:
        return

    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R

    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(
            body.image,
            window_width + r,
            window_height + r,
            window_width + 2 * r,
            window_height + 2 * r
        )
        return

    space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")