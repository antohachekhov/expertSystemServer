from ExpertSytemModel.patients import Patient
from ExpertSytemModel.projects import Project


class PatientsActual(Patient):
    """
    Фактические пациенты
    """

    def __init__(self, patient: Patient, project: Project = None):
        super().__init__(patient.haveConditions, patient.haveNotConditions, patient.behavior)
        self.project = project

    def dict(self):
        superDict = super().dict()
        selfDict = superDict | {'project': self.project.dict()}
        return selfDict


class PatientsNegative(PatientsActual):
    """
    Отрицательные пациенты
    """
    pass


class PatientsPositive(PatientsActual):
    """
    Положительные пациенты
    """
    pass


class PatientsSatisfactory(PatientsActual):
    """
    Удовлетворительные пациенты
    """
    pass
