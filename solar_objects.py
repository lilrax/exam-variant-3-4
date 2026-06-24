# coding: utf-8
# license: GPLv3

"""Модуль с классами космических объектов.

Здесь реализуется часть ООП-рефакторинга проекта:
- общий базовый класс SpaceObject;
- наследование классов Star и Planet от SpaceObject;
- инкапсуляция через свойства;
- общий интерфейс для объектов.
"""


class SpaceObject:
    """Базовый класс для всех космических объектов.

    Содержит общие поля: массу, координаты, скорость, силу,
    визуальный радиус, цвет и ссылку на изображение на Canvas.
    """

    type = "space_object"

    def __init__(
        self,
        radius=5,
        color="white",
        mass=0,
        x=0,
        y=0,
        vx=0,
        vy=0,
    ):
        """Создаёт космический объект с начальными параметрами."""
        self._radius = radius
        self._mass = mass
        self._x = x
        self._y = y
        self.Vx = vx
        self.Vy = vy
        self.Fx = 0
        self.Fy = 0
        self.color = color
        self.image = None

    @property
    def R(self):
        """Возвращает радиус объекта."""
        return self._radius

    @R.setter
    def R(self, value):
        if value <= 0:
            raise ValueError("Радиус объекта должен быть положительным")
        self._radius = value

    @property
    def m(self):
        """Возвращает массу объекта."""
        return self._mass

    @m.setter
    def m(self, value):
        if value < 0:
            raise ValueError("Масса объекта не может быть отрицательной")
        self._mass = value

    @property
    def x(self):
        """Возвращает координату x."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Возвращает координату y."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def set_position(self, x, y):
        """Устанавливает координаты объекта."""
        self.x = x
        self.y = y

    def set_velocity(self, vx, vy):
        """Устанавливает скорость объекта."""
        self.Vx = vx
        self.Vy = vy

    def set_force(self, fx, fy):
        """Устанавливает силу, действующую на объект."""
        self.Fx = fx
        self.Fy = fy


class Star(SpaceObject):
    """Тип данных, описывающий звезду.

    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"

    def __init__(
        self,
        radius=5,
        color="red",
        mass=0,
        x=0,
        y=0,
        vx=0,
        vy=0,
    ):
        """Создаёт объект звезды."""
        super().__init__(
            radius=radius,
            color=color,
            mass=mass,
            x=x,
            y=y,
            vx=vx,
            vy=vy,
        )


class Planet(SpaceObject):
    """Тип данных, описывающий планету.

    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет.
    """

    type = "planet"

    def __init__(
        self,
        radius=5,
        color="green",
        mass=0,
        x=0,
        y=0,
        vx=0,
        vy=0,
    ):
        """Создаёт объект планеты."""
        super().__init__(
            radius=radius,
            color=color,
            mass=mass,
            x=x,
            y=y,
            vx=vx,
            vy=vy,
        )