import json
from ExpertSytemModel.behavior import Behavior


class Patient:
    def __init__(self, haveContidions=None, haveNotCondition=None, behavior:Behavior=None):
        self.haveConditions = list() if haveContidions is None else haveContidions
        self.haveNotConditions = list() if haveNotCondition is None else haveNotCondition
        self.behavior = behavior

    def dict(self):
        return {
            'haveConditions': [condition.value for condition in self.haveConditions],
            'haveNotConditions': [condition.value for condition in self.haveNotConditions],
            'behavior': None if self.behavior is None else self.behavior.value
        }
