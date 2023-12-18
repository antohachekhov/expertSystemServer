class User:
    def __init__(self, name):
        self.name = name

    def dict(self):
        return {
            'name': self.name
        }


class UserSupportStaff(User):
    """
    Вспомогательный персонал
    """
    pass


class UserResearchAssociate(User):
    """
    Научные сотрудники
    """
    pass


class UserSecurityService(User):
    """
    Служба безопасности
    """
    pass


class UserResponseTeam(User):
    """
    Члены группы реагирования
    """
    pass


class UserThaumiel(User):
    """
    Члены совета Таумиэль
    """
    pass


dictUsers = {
    'Психолог': UserSupportStaff('Психолог'),
    'Медсестра': UserSupportStaff('Медсестра'),
    'Лаборант': UserSupportStaff('Лаборант'),
    'Ученый': UserResearchAssociate('Ученый'),
    'Аспирант': UserResearchAssociate('Аспирант'),
    'Охранник': UserSecurityService('Охранник'),
    'Спецназовец': UserResponseTeam('Спецназовец'),
    'Член совета Таумиэль': UserThaumiel('Член совета Таумиэль')
}