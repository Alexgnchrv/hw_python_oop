from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration_hours = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hours

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'{self.__str__()} subclass should implement this!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__str__(),
                           self.duration_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )

    def __str__(self) -> str:
        return f'{self.__class__.__name__}'


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight_kg / self.M_IN_KM
            * (self.duration_hours * self.M_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_SECOND_MULTIPLIER: float = 0.029
    HEIGHT_DIVIDER: int = 100
    SPEED_ROOT: int = 2
    SPEED_MULTIPLIER: float = 0.278

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
                + ((self.get_mean_speed() * self.SPEED_MULTIPLIER)
                 ** self.SPEED_ROOT / (self.height / self.HEIGHT_DIVIDER))
                * self.CALORIES_WEIGHT_SECOND_MULTIPLIER
                * self.weight_kg) * (self.duration_hours * self.M_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    SPEED_ROOT: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_hours)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.SPEED_ROOT * self.weight_kg * self.duration_hours)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    codes: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in codes.keys():
        raise Exception('Такого типа упражнений нет в словаре')
    return codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Имитация получения данных от блока датчиков фитнес-трекера"""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
