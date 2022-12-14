from dataclasses import dataclass


def toFixed(numObj, digits=0):
    """
    Функция для округления с фиксированным числом знаков после запятой,
    даже если в конце только нули.
    Необходима, так как встроенная функция round() оставшиеся нули обрезает
    """
    return f"{numObj:.{digits}f}"


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Составить информационное сообщение о выполненной тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {toFixed(self.duration, 3)} ч.; '
                f'Дистанция: {toFixed(self.distance, 3)} км; '
                f'Ср. скорость: {toFixed(self.speed, 3)} км/ч; '
                f'Потрачено ккал: {toFixed(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.'
                                  % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.__class__.__name__,
                                    self.duration, self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIE_1 = 18
        COEFF_CALORIE_2 = 20
        MIN_IN_H = 60

        return ((COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration * MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        WEIGHT_COEFF = 0.035
        HEIGHT_COEFF = 0.029
        MIN_IN_H = 60

        return (WEIGHT_COEFF * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * HEIGHT_COEFF * self.weight) * self.duration * MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_SPEED = 1.1
        COEFF_SWIMMING_WEIGHT = 2

        return ((self.get_mean_speed() + COEFF_SPEED)
                * COEFF_SWIMMING_WEIGHT * self.weight)

    def get_mean_speed(self) -> float:
        """Получить дистанцию в км."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'SWM': Swimming, 'WLK': SportsWalking, 'RUN': Running}
    try:
        return workout_type_dict[workout_type](*data)
    except KeyError:
        raise ValueError(f'Тренировки {workout_type} не существует.'
                         ' Проверьте правильность введённых данных')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1206, 12, 6]),
        ('WLK', [9000, 10, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except ValueError:
            print('Ошибка! Проверьте правильность введённых данных')
