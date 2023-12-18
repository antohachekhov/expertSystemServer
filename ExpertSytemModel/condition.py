class Condition:
    def __init__(self, value: str):
        self.value = value

    def dict(self):
        return self.value


class ConditionWhite(Condition):
    pass


class ConditionActualPatients(Condition):
    pass


class ConditionGreen(ConditionActualPatients):
    pass


class ConditionRed(ConditionActualPatients):
    pass


class ConditionOrange(ConditionActualPatients):
    pass

"""
dictConditions = {
    'Кома': Condition('Кома'),
    'Паралич': Condition(),
    'Не подает признаков жизни': Condition(),
    'Температура низкая': Condition(),
    'Температура средняя': Condition(),
    'Температура высокая': Condition(),
    'Давление низкое': Condition(),
    'Давление среднее': Condition(),
    'Давление высокое': Condition(),
    'Пульс низкий': Condition(),
    'Пульс средний': Condition(),
    'Пульс высокий': Condition(),
    'Ступор': Condition(),
    'Судороги': Condition(),
    'Стонет': Condition(),
    'Бредит': Condition(),
    'Аллергическая реакция': Condition(),
    'Задыхается': Condition(),
    'Лихорадка': Condition(),
    'Нарушение одного из 5ти чувств': Condition(),
    'Активен': Condition(),
}
"""