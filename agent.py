from abc import ABC, abstractmethod

from dataset import Dataset
from preference import Preference
from proposal import Proposal


class Agent(ABC):

    def __init__(self, dataset : Dataset, preference : Preference):
        self.dataset = dataset
        preference.normalize_weights()
        self.preference = preference
        self.my_previous_proposal = None
        self.opponent_previous_proposal = None
    
    @abstractmethod
    def evaluate_proposal(self, proposal : Proposal) -> Proposal | None:
        pass

    def accept_proposal(self, proposal : Proposal):
        pass

    def reject_proposal(self, proposal : Proposal):
        pass
