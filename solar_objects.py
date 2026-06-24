# coding: utf-8
# license: GPLv3

"""Модуль с классами космических объектов.

В модуле реализована ООП-модель:
- SpaceObject — общий базовый класс;
- Star — звезда;
- OrbitingObject — объект, вращающийся по орбите;
- Planet — планета;
- Satellite — спутник.

Так показываются принципы ООП:
- абстракция: общий класс SpaceObject;
- наследование: Star, Planet, Satellite наследуются от базовых классов;
- инкапсуляция: поля радиуса, массы и координат доступны через свойства;
- полиморфизм: метод update_position переопределяется у разных классов.
"""

from math import cos, sin


class SpaceObject:
    """Базовый класс для всех космических объектов."""

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
        self.orbit_image = None

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

    def update_position(self, dt):
        """Обновляет положение объекта.

        Для базового объекта метод ничего не делает.
        Дочерние классы могут переопределять это поведение.
        """

        return None


class Star(SpaceObject):
    """Класс звезды."""

    type = "star"

    def __init__(
        self,
        radius=18,
        color="yellow",
        mass=1.0E30,
        x=0,
        y=0,
        vx=0,
        vy=0,
        name="Star",
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
        self.name = name
        self.planets = []

    def add_planet(self, planet):
        """Добавляет планету к звезде."""

        self.planets.append(planet)


class OrbitingObject(SpaceObject):
    """Базовый класс объекта, который вращается вокруг центра."""

    type = "orbiting_object"

    def __init__(
        self,
        radius=5,
        color="white",
        mass=1,
        center=None,
        orbit_radius=100,
        angle=0,
        angular_speed=0.01,
        direction=1,
        name="Orbiting object",
    ):
        """Создаёт объект, движущийся по круговой орбите."""

        super().__init__(
            radius=radius,
            color=color,
            mass=mass,
        )

        self.center = center
        self.orbit_radius = orbit_radius
        self.angle = angle
        self.angular_speed = angular_speed
        self.direction = direction
        self.name = name

        self.update_position(0)

    def get_center_coordinates(self):
        """Возвращает координаты центра вращения."""

        if self.center is None:
            return 0, 0

        return self.center.x, self.center.y

    def update_position(self, dt):
        """Пересчитывает положение объекта на орбите."""

        self.angle += self.direction * self.angular_speed * dt

        center_x, center_y = self.get_center_coordinates()

        self.x = center_x + self.orbit_radius * cos(self.angle)
        self.y = center_y + self.orbit_radius * sin(self.angle)


class Planet(OrbitingObject):
    """Класс планеты."""

    type = "planet"

    def __init__(
        self,
        radius=5,
        color="green",
        mass=1.0E24,
        center=None,
        orbit_radius=100,
        angle=0,
        angular_speed=0.01,
        direction=1,
        name="Planet",
    ):
        """Создаёт объект планеты."""

        super().__init__(
            radius=radius,
            color=color,
            mass=mass,
            center=center,
            orbit_radius=orbit_radius,
            angle=angle,
            angular_speed=angular_speed,
            direction=direction,
            name=name,
        )

        self.satellites = []

    def add_satellite(self, satellite):
        """Добавляет спутник к планете."""

        self.satellites.append(satellite)


class Satellite(OrbitingObject):
    """Класс спутника планеты."""

    type = "satellite"

    def __init__(
        self,
        radius=2,
        color="white",
        mass=1.0E20,
        center=None,
        orbit_radius=18,
        angle=0,
        angular_speed=0.04,
        direction=1,
        name="Satellite",
    ):
        """Создаёт объект спутника."""

        super().__init__(
            radius=radius,
            color=color,
            mass=mass,
            center=center,
            orbit_radius=orbit_radius,
            angle=angle,
            angular_speed=angular_speed,
            direction=direction,
            name=name,
        )