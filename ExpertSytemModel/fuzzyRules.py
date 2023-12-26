
class Fuzzification:
    def __init__(self, left: list, center: list, right: list):
        self.intervalLeft = left
        self.intervalCenter = center
        self.intervalRight = right

    def farLeft(self, x) -> float:
        if x <= self.intervalLeft[0]:
            return 1.0
        elif self.intervalLeft[0] < x < self.intervalLeft[1]:
            return (self.intervalLeft[1] - x) / (self.intervalLeft[1] - self.intervalLeft[0])
        else:
            return 0.0

    def farRight(self, x) -> float:
        if x <= self.intervalRight[0]:
            return 0.0
        elif self.intervalRight[0] < x < self.intervalRight[1]:
            return (x - self.intervalRight[0]) / (self.intervalRight[1] - self.intervalRight[0])
        else:
            return 1.0

    def triangle(self, x) -> float:
        if self.intervalCenter[0] < x <= self.intervalCenter[1]:
            return (x - self.intervalCenter[0]) / (self.intervalCenter[1] - self.intervalCenter[0])
        elif self.intervalCenter[1] < x <= self.intervalCenter[2]:
            return (self.intervalCenter[2] - x) / (self.intervalCenter[2] - self.intervalCenter[1])
        else:
            return 0.0

    def __call__(self, x, *args, **kwargs) -> tuple:
        return self.farLeft(x), self.triangle(x), self.farRight(x)


class FuzzyLogic:
    names = ['Positive', 'Satisfactory', 'Negative']
    numToColor = {0 : 'green',
                  1: 'orange',
                  2: 'red'}

    inverseStatus = {'Positive': 'Negative',
                     'Negative': 'Positive',
                     'Satisfactory': 'Satisfactory'}

    def __init__(self, functions: dict):
        self.greens = Fuzzification(*functions['greens'])
        self.orange = Fuzzification(*functions['orange'])
        self.reds = Fuzzification(*functions['reds'])

    def __call__(self, countGreen, countOrange, countRed, *args, **kwargs):
        results = {color:
                       {name: value for name, value in zip(FuzzyLogic.names, fuzzyClass)}
                   for color, fuzzyClass in zip(['green', 'orange', 'red'],
                                                [self.greens(countGreen), self.orange(countOrange), self.reds(countRed)])}

        print(f'greens: {results["green"]}')
        print(f'orange: {results["orange"]}')
        print(f'reds: {results["red"]}')

        keysForMaxValue = [max(results[f], key=lambda x: results[f][x])for f in results]

        minValue = results['green'][keysForMaxValue[0]]
        minIndex = 0

        for index, value in enumerate(keysForMaxValue[1:]):
            if results[FuzzyLogic.numToColor[index + 1]][value] < minValue:
                minValue = results[FuzzyLogic.numToColor[index + 1]][value]
                minIndex = index + 1

        resultStatus = keysForMaxValue[minIndex]
        if FuzzyLogic.numToColor[minIndex] == 'green':
            resultStatus = FuzzyLogic.inverseStatus[resultStatus]

        return FuzzyLogic.numToColor[minIndex], resultStatus, minValue



