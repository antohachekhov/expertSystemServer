from ExpertSytemModel.patients import *


class Protocol:
    def __init__(self, name: str, reaction: str):
        self.name = name
        self.reaction = reaction
        pass

    def dict(self):
        return {
            'name': self.name,
            'reaction': self.reaction
        }

class ProtocolCalled(Protocol):
    pass


class ProtocolDisplayed(ProtocolCalled):
    pass



dictProtocol = {
    'Идиллия': Protocol('Идиллия', 'Расслабитесь'),
    'Спок-Нок': Protocol('Спок-Нок', 'Срочно вколоть полезные вещества'),
    'Эйрена': Protocol('Эйрена', 'Пациенту был вколот транквилизатор, отправка на дополнительные исследования'),
    'Катарина': Protocol('Катарина', 'Нейтрализация пациента'),
    'Тиран': Protocol('Тиран', 'Нейтрализация группы пациентов'),
    'Корона': Protocol('Корона', 'Объявление карантина в лаборатории'),
    'Селена': Protocol('Селена', ''),
    'Амария': Protocol('Амария', 'Глобальные последствия, утечка'),
    'Аид': Protocol('Аид', 'Зачистка сотрудников и пациентов лаборатории'),
    'Красная Королева': Protocol('Красная Королева', 'Передача управления лабораторией ИИ'),
    'Модсли': Protocol('Модсли', 'Запуск процесса восстановления')
}
