from ExpertSytemModel.patients import Patient
from ExpertSytemModel.condition import Condition


class PatientsExpected(Patient):
    """
    Ожидаемые пациенты
    """

    def __init__(self, greenConditions, orangeConditions, redConditions):
        Patient.__init__(self, greenConditions + orangeConditions + redConditions, None)
        self.greenConditions = greenConditions
        self.orangeConditions = orangeConditions
        self.redConditions = redConditions

    def dict(self):
        superDict = super().dict()
        selfDict = superDict | {'greenConditions': [condition.value for condition in self.greenConditions],
                                'orangeConditions': [condition.value for condition in self.orangeConditions],
                                'redConditions': [condition.value for condition in self.redConditions]}
        return selfDict


dictPatients = {
    'Энигма': PatientsExpected([Condition(cond) for cond in ['Кома', 'Паралич', 'Не подает признаков жизни', 'Температура средняя',
                                'Давление низкое', 'Пульс низкий', 'Ступор']],
                               [Condition(cond) for cond in ['Судороги', 'Стонет', 'Бредит']],
                               [Condition(cond) for cond in ['Аллергическая реакция', 'Задыхается', 'Лихорадка', 'Нарушение одного из 5ти чувств',
                                'Активен', 'Температура низкая', 'Температура средняя', 'Давление среднее',
                                'Давление высокое', 'Пульс средний', 'Пульс высокий']]),

    'Сороконожка': PatientsExpected([Condition(cond) for cond in ['Активен', 'Температура средняя', 'Давление высокое',
                                                                  'Пульс высокий', 'Стонет']],
                                    [Condition(cond) for cond in ['Нарушение одного из 5ти чувств', 'Бредит', 'Судороги']],
                                    [Condition(cond) for cond in ['Задыхается', 'Ступор', 'Паралич', 'Аллергическая реакция', 'Кома', 'Лихорадка',
                                     'Не подает признаков жизни', 'Температура низкая', 'Температура высокая',
                                     'Давление среднее', 'Давление низкое', 'Пульс средний', 'Пульс низкий']]),

    'Зимний солдат': PatientsExpected([Condition(cond) for cond in ['Активен', 'Температура низкая', 'Давление высокое',
                                                                    'Пульс низкий', 'Стонет', 'Бредит']],
                                      [Condition(cond) for cond in ['Нарушение одного из 5ти чувств', 'Судороги']],
                                      [Condition(cond) for cond in ['Задыхается', 'Ступор', 'Паралич',
                                                                    'Аллергическая реакция', 'Кома', 'Лихорадка',
                                       'Не подает признаков жизни', 'Температура высокая', 'Температура средняя',
                                       'Давление среднее', 'Давление низкое', 'Пульс средний', 'Пульс высокий']]),

    'Ультимо': PatientsExpected([Condition(cond) for cond in ['Активен', 'Температура низкая', 'Давление низкое',
                                                              'Пульс низкий']],
                                [Condition(cond) for cond in ['Ступор', 'Кома', 'Не подает признаков жизни']],
                                [Condition(cond) for cond in ['Стонет', 'Бредит', 'Задыхается', 'Паралич', 'Аллергическая реакция', 'Лихорадка',
                                 'Нарушение одного из 5ти чувств', 'Судороги', 'Температура высокая',
                                 'Температура средняя', 'Давление среднее', 'Давление высокое', 'Пульс средний',
                                 'Пульс высокий']]),

    'Кордицепс': PatientsExpected([Condition(cond) for cond in ['Активен', 'Температура высокая', 'Давление высокое', 'Пульс высокий', 'Стонет',
                                   'Бредит', 'Ступор']],
                                  [Condition(cond) for cond in ['Нарушение одного из 5ти чувств', 'Судороги', 'Задыхается', 'Паралич',
                                   'Аллергическая реакция', 'Лихорадка', 'Кома']],
                                  [Condition(cond) for cond in ['Не подает признаков жизни', 'Температура низкая', 'Температура средняя',
                                   'Давление среднее', 'Давление низкое', 'Пульс средний', 'Пульс низкий']]),

    'Таити': PatientsExpected([Condition(cond) for cond in ['Активен', 'Температура высокая', 'Давление высокое',
                                                            'Пульс высокий', 'Стонет', 'Бредит',
                                                            'Нарушение одного из 5ти чувств', 'Судороги',
                                                            'Аллергическая реакция']],
                              [Condition(cond) for cond in ['Ступор', 'Задыхается', 'Паралич', 'Лихорадка', 'Кома']],
                              [Condition(cond) for cond in ['Не подает признаков жизни', 'Температура низкая',
                                                            'Температура средняя', 'Давление среднее',
                                                            'Давление низкое', 'Пульс средний', 'Пульс низкий']])
}
