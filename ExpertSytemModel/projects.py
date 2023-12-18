from ExpertSytemModel.patientsExpected import PatientsExpected, dictPatients


class Project:
    def __init__(self, expectedPatient: PatientsExpected, projectName):
        self.expectedPatient = expectedPatient
        self.name = projectName

    def dict(self):
        return {'expectedPatient': self.expectedPatient.dict()}

class ProjectEuclid(Project):
    pass


class ProjectKeter(Project):
    pass


class ProjectKeterAlfa(ProjectKeter):
    pass


class ProjectKeterBeta(ProjectKeter):
    pass


class ProjectKeterOmega(ProjectKeter):
    pass


class ProjectSafer(Project):
    pass


dictProjects = {
    'Зимний солдат': ProjectKeterAlfa(dictPatients['Зимний солдат'], 'Зимний солдат'),
    'Сороконожка': ProjectKeterBeta(dictPatients['Сороконожка'], 'Сороконожка'),
    'Кордицепс': ProjectEuclid(dictPatients['Кордицепс'], 'Кордицепс'),
    'Ультимо': ProjectKeterOmega(dictPatients['Ультимо'], 'Ультимо'),
    'Таити': ProjectEuclid(dictPatients['Таити'], 'Таити'),
    'Энигма': ProjectSafer(dictPatients['Энигма'], 'Энигма')
}