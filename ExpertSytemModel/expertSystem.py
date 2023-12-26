from ExpertSytemModel.patientsActual import PatientsActual, PatientsPositive, PatientsNegative, PatientsSatisfactory
import json
from ExpertSytemModel.projects import dictProjects, ProjectEuclid, ProjectKeterAlfa, ProjectKeterBeta, \
    ProjectKeterOmega, ProjectSafer
from ExpertSytemModel.patients import Patient
from ExpertSytemModel.condition import Condition, ConditionGreen, ConditionOrange, ConditionRed, ConditionWhite
from ExpertSytemModel.behavior import Behavior
from ExpertSytemModel.protocols import Protocol, dictProtocol
from ExpertSytemModel.users import dictUsers, UserResearchAssociate, UserResponseTeam, UserSecurityService, \
    UserSupportStaff, UserThaumiel
from ExpertSytemModel.fuzzyRules import FuzzyLogic


class ExpertSystem:
    # setProjectToPatientQuestionID = 'project_q_2'

    def __init__(self):
        self.currentUser = None
        self.actualProtocols = list()
        self.displayedProtocols = list()
        self.patient = Patient()
        self.project = None

        with open(r'ExpertSytemModel\questions.json', 'r', encoding='utf-8') as file:
            self.questions = json.loads(file.read())

        self._dictCommand = {
            'patient': self._setConditionsOrBehavorToPatient,
            'project': self._setProjectToPatient,
            'user': self._setUser
        }

        self.fuzzyLogic = FuzzyLogic({'greens': [[0, 1], [0, 1, 6], [1, 7]],
                                      'orange': [[0, 1.5], [0, 1.5, 3], [1.5, 3]],
                                      'reds': [[0, 1], [0, 1, 11], [1, 11]]})

    def dict(self):
        return {
            "currentUser": 'None' if self.currentUser is None else self.currentUser.dict(),
            "actualProtocols": 'None' if len(self.actualProtocols) == 0 else [protocol.dict() for protocol in
                                                                              self.actualProtocols],
            "displayedProtocols": 'None' if len(self.displayedProtocols) == 0 else [protocol.dict() for protocol in
                                                                                    self.displayedProtocols],
            "patient": 'None' if self.patient is None else self.patient.dict()
        }

    def answer(self, request) -> str:
        questionID = request['questionId']
        answersID = request['answersId']
        command = self._dictCommand.get(questionID.split('_')[0])
        if command is None:
            raise Exception('400 Не верный ID вопроса')
        command(questionID, answersID)
        return json.dumps(self.dict())

    def getResult(self):
        countGreen = 0
        countOrange = 0
        countRed = 0
        specialCondValue = ''
        specialCond = None
        projectName = self.patient.project.name
        isActive = False
        if projectName == 'Энигма':
            specialCond = 'Активен'
        elif projectName == 'Сороконожка' or projectName == 'Зимний солдат':
            specialCond = 'Не подает признаков жизни'
        for cond in self.patient.haveConditions:
            if cond.value == 'Активен':
                isActive = True
            typeCond = type(cond)
            if cond.value == specialCondValue:
                specialCond = cond
            if typeCond is ConditionGreen:
                countGreen += 1
            elif typeCond is ConditionOrange:
                countOrange += 1
            elif typeCond is ConditionRed:
                countRed += 1

        if type(self.patient.project) is ProjectSafer:
            if not isActive:
                if 'A' in self.patient.behavior.value.split('код ')[1]:
                    raise Exception('400 Пациент не агресивничает, когда находится в коме!!!')

            if (
                    self.patient.behavior.value == 'Положительно спокоен (код C1)' or self.patient.behavior.value == "Апатичен (код C2)") and countRed == 0:
                self.actualProtocols.append(dictProtocol['Идиллия'])
            elif countRed > 0 and (
                    self.patient.behavior.value == 'Положительно спокоен (код C1)' or self.patient.behavior.value == "Апатичен (код C2)" or \
                    self.patient.behavior.value == 'Пассивная агрессия (код A1)' or self.patient.behavior.value == "Угрозы в адрес сотрудников или других пациентов (код A2)"):
                self.actualProtocols.append(dictProtocol['Спок-Нок'])
            elif isActive and self.patient.behavior.value == 'Агрессия, направленная на предметы (код A3)' or \
                    self.patient.behavior.value == "Нападение на людей (код A4)":
                self.actualProtocols.append(dictProtocol['Эйрена'])
            elif isActive and countRed > 0 and self.patient.behavior.value == 'Нападение на людей с летальным исходом (код A5)' or \
                    self.patient.behavior.value == "Агрессия, направленная на себя (код A0)":
                self.actualProtocols.append(dictProtocol['Катарина'])

        elif type(self.patient.project) is ProjectEuclid:
            if type(self.patient) is PatientsPositive and (
                    self.patient.behavior.value == 'Положительно спокоен (код C1)' or self.patient.behavior.value == "Апатичен (код C2)" or \
                    self.patient.behavior.value == 'Пассивная агрессия (код A1)'):
                self.actualProtocols.append(dictProtocol['Идиллия'])
            elif type(self.patient) in [PatientsPositive,
                                        PatientsSatisfactory] and self.patient.behavior.value == 'Угрозы в адрес сотрудников или других пациентов (код A2)':
                self.actualProtocols.append(dictProtocol['Спок-Нок'])
            elif self.patient.behavior.value == 'Агрессия, направленная на предметы (код A3)':
                self.actualProtocols.append(dictProtocol['Эйрена'])
            elif self.patient.behavior.value == 'Нападение на людей (код A4)' or self.patient.behavior.value == 'Агрессия, направленная на себя (код A0)':
                self.actualProtocols.append(dictProtocol['Катарина'])
            elif self.patient.behavior.value == 'Нападение на людей с летальным исходом (код A5)':
                self.actualProtocols.append(dictProtocol['Тиран'])

        elif type(self.patient.project) in [ProjectKeterAlfa, ProjectKeterBeta, ProjectKeterOmega]:
            if type(self.patient) in [PatientsPositive] and (
                    self.patient.behavior.value == 'Положительно спокоен (код C1)' or self.patient.behavior.value == "Апатичен (код C2)" or \
                    self.patient.behavior.value == 'Пассивная агрессия (код A1)'):
                self.actualProtocols.append(dictProtocol['Идиллия'])
            elif type(self.patient) in [PatientsPositive,
                                        PatientsSatisfactory] and self.patient.behavior.value == 'Угрозы в адрес сотрудников или других пациентов (код A2)':
                self.actualProtocols.append(dictProtocol['Спок-Нок'])
            elif type(self.patient.project) is ProjectKeterAlfa:
                if 'A3' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Эйрена'])
                elif 'A4' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Катарина'])
                elif 'A5' in self.patient.behavior.value or 'A0' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Тиран'])
            elif type(self.patient.project) is ProjectKeterBeta:
                if 'A3' in self.patient.behavior.value or 'A4' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Эйрена'])
                elif 'A0' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Катарина'])
                elif 'A5' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Тиран'])
            elif type(self.patient.project) is ProjectKeterOmega:
                if 'A3' in self.patient.behavior.value or 'A4' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Эйрена'])
                elif 'A5' in self.patient.behavior.value or 'A0' in self.patient.behavior.value:
                    self.actualProtocols.append(dictProtocol['Катарина'])

        if self.patient.project.name in ["Кордицепс", "Таити", "Сороконожка"]:
            if type(self.patient.project) in [ProjectEuclid, ProjectKeterBeta]:
                if type(self.patient) in [PatientsSatisfactory, PatientsNegative] and (
                        'A4' in self.patient.behavior.value or 'A5' in self.patient.behavior.value):
                    self.actualProtocols.append(dictProtocol['Корона'])

        if self.patient.project.name == 'Сороконожка' and 'Тиран' in [protocol.name for protocol in
                                                                      self.actualProtocols]:
            self.actualProtocols.append(dictProtocol['Селена'])

        if self.patient.project.name == 'Зимний солдат' and (
                'Тиран' in [protocol.name for protocol in self.actualProtocols] or 'Катарина' in [protocol.name for
                                                                                                  protocol in
                                                                                                  self.actualProtocols]):
            self.actualProtocols.append(dictProtocol['Селена'])

        if (self.patient.project.name == 'Кордицепс' or self.patient.project.name == 'Таити') and (
                'Катарина' in [protocol.name for protocol in self.actualProtocols]):
            self.actualProtocols.append(dictProtocol['Селена'])

        if (self.patient.project.name == 'Кордицепс' or self.patient.project.name == 'Таити') and (
                'Тиран' in [protocol.name for protocol in self.actualProtocols]):
            self.actualProtocols.append(dictProtocol['Аид'])
            self.actualProtocols.append(dictProtocol['Красная Королева'])
            self.actualProtocols.append(dictProtocol['Амария'])
            self.actualProtocols.append(dictProtocol['Модсли'])

        if 'Модсли' not in [protocol.name for protocol in self.actualProtocols] and 'Идиллия' not in [protocol.name for
                                                                                                      protocol in
                                                                                                      self.actualProtocols]:
            self.actualProtocols.append(dictProtocol['Идиллия'])

        self.displayedProtocols = self.actualProtocols.copy()

        if type(self.currentUser) is UserSupportStaff:
            if self.actualProtocols[0].name == 'Эйрена':
                self.displayedProtocols[0] = dictProtocol['Спок-Нок']

        if type(self.currentUser) in [UserResearchAssociate, UserSupportStaff]:
            if self.actualProtocols[0].name == 'Катарина':
                self.displayedProtocols[0] = dictProtocol['Спок-Нок']

        if type(self.currentUser) in [UserResearchAssociate, UserSupportStaff, UserSecurityService]:
            if self.actualProtocols[0].name == 'Тиран':
                self.displayedProtocols[0] = dictProtocol['Эйрена']

        if type(self.currentUser) != UserThaumiel:
            if self.actualProtocols[-1].name == 'Модсли':
                self.displayedProtocols[-1] = dictProtocol['Идиллия']

            index = 0
            while index < len(self.actualProtocols):
                if index < len(self.displayedProtocols):
                    print([protocol.name for protocol in self.displayedProtocols])
                    if self.displayedProtocols[index].name in ['Амария', 'Селена', 'Аид', 'Красная Королева']:
                        self.displayedProtocols = self.displayedProtocols[0:index] + self.displayedProtocols[index + 1:]
                        index -= 1
                else:
                    break
                index += 1

        return json.dumps(self.dict())

    def _setProjectToPatient(self, questionID, answerID):
        for project in self.questions['project']:
            if project['id'] == questionID:
                for answer in project['answers']:
                    if answer['id'] == answerID[0]:
                        self.patient = PatientsActual(self.patient, dictProjects[answer['text']])
                        self.changeColorForActualConditions()
                        # return json.dumps(self.dict())
                        return 1
                raise Exception('500 Не найден ответ')
        raise Exception('500 Не найден вопрос')

    def _getAnswersFromJSON(self, category, categoryID):
        if category not in self.questions:
            raise Exception('500 Не найдена категория')

        questions = {question['id']: question['answers'] for question in self.questions[category]}
        if categoryID not in questions:
            raise Exception('500 Не найден вопрос')
        return {
            answer['id']: answer['text'] for answer in questions[categoryID]
        }

    def _setConditionsOrBehavorToPatient(self, questionID, answersID):
        if questionID == 'patient_q_1':
            return self._setConditionsToPatient(questionID, answersID)
        elif questionID == 'patient_q_2':
            return self._setBehaviorToPatient(questionID, answersID[0])
        raise Exception('400 Не верный ID вопроса')

    def _setConditionsToPatient(self, questionID, answersID):
        answers = self._getAnswersFromJSON('patient', questionID)
        for answerID in answersID:
            isGreen = True if answerID.split('_')[-1] == 'green' else False
            cleanAnswerID = '_'.join(answerID.split('_')[:-1])
            if cleanAnswerID not in answers:
                raise Exception('500 Не найден ответ')
            if isGreen:
                self.patient.haveConditions.append(Condition(answers[cleanAnswerID]))
            else:
                self.patient.haveNotConditions.append(Condition(answers[cleanAnswerID]))

        self.changeColorForActualConditions()
        # return json.dumps(self.dict())

    def _setBehaviorToPatient(self, questionID, answersID):
        answers = self._getAnswersFromJSON('patient', questionID)
        if answersID not in answers:
            raise Exception('500 Не найден ответ')
        self.patient.behavior = Behavior(answers[answersID])
        # return json.dumps(self.dict())

    def _setUser(self, questionID, answersID):
        answers = self._getAnswersFromJSON('user', questionID)
        if answersID[0] not in answers:
            raise Exception('500 Не найден ответ')
        self.currentUser = dictUsers[answers[answersID[0]]]

    def getColorForActualCondition(self, condition):
        if condition in [cond.value for cond in self.patient.project.expectedPatient.greenConditions]:
            return ConditionGreen(condition)
        elif condition in [cond.value for cond in self.patient.project.expectedPatient.orangeConditions]:
            return ConditionOrange(condition)
        elif condition in [cond.value for cond in self.patient.project.expectedPatient.redConditions]:
            return ConditionRed(condition)
        else:
            return ConditionWhite(condition)

    def changeColorForActualConditions(self):
        if isinstance(self.patient, PatientsActual):
            if self.patient.project is not None:
                if self.patient.haveConditions is not None:
                    coloredHaveCondition = list()
                    for condition in self.patient.haveConditions:
                        coloredHaveCondition.append(self.getColorForActualCondition(condition.value))
                    self.patient.haveConditions = coloredHaveCondition
                if self.patient.haveNotConditions is not None:
                    coloredHaveNotCondition = list()
                    for condition in self.patient.haveNotConditions:
                        coloredHaveNotCondition.append(self.getColorForActualCondition(condition.value))
                    self.patient.haveNotConditions = coloredHaveNotCondition
                self.defineClassPatient()

    def defineClassPatient(self):
        if isinstance(self.patient, PatientsActual):
            countGreen = 0
            countOrange = 0
            countRed = 0
            specialCondValue = ''
            specialCond = None
            projectName = self.patient.project.name
            if projectName == 'Энигма':
                specialCond = 'Активен'
            elif projectName == 'Сороконожка' or projectName == 'Зимний солдат':
                specialCond = 'Не подает признаков жизни'
            for cond in self.patient.haveConditions:
                typeCond = type(cond)
                if cond.value == specialCondValue:
                    specialCond = cond
                if typeCond is ConditionGreen:
                    countGreen += 1
                elif typeCond is ConditionOrange:
                    countOrange += 1
                elif typeCond is ConditionRed:
                    countRed += 1

            color, status, value = self.fuzzyLogic(countGreen, countOrange, countRed)

            print(f"{color} - {status} - {value}")

            if status == 'Negative':
                self.patient = PatientsNegative(self.patient, self.patient.project)
            elif status == 'Satisfactory':
                self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            else:
                self.patient = PatientsPositive(self.patient, self.patient.project)

            # if projectName == 'Энигма':
            #     if countGreen == 7 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1 and specialCond is None:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2 and specialCond is not None:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            # elif projectName == 'Сороконожка':
            #     if countGreen == 5 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1 and specialCond is None:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2 and specialCond is not None:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            # elif projectName == 'Зимний солдат':
            #     if countGreen == 6 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1 and specialCond is None:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2 and specialCond is not None:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            # elif projectName == 'Ультимо':
            #     if countGreen == 4 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            # elif projectName == 'Кордицепс':
            #     if countGreen == 7 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            # elif projectName == 'Таити':
            #     if countGreen == 9 and countOrange == 0 and countRed == 0:
            #         self.patient = PatientsPositive(self.patient, self.patient.project)
            #     elif countRed == 0 and countOrange >= 1 or countOrange == 0 and countRed == 1:
            #         self.patient = PatientsSatisfactory(self.patient, self.patient.project)
            #     elif countRed >= 2:
            #         self.patient = PatientsNegative(self.patient, self.patient.project)
            print(f'Тип пациента изменён на {type(self.patient)}')
