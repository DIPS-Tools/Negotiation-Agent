import random
from agent import Agent
from dataset import Dataset
from dpv import get_purpose_detail
from odrl import get_action_detail
from preference import Preference
from proposal import Proposal
from rule import Rule


class ConsumerAgent(Agent):
    
    def __init__(self, dataset : Dataset, preference : Preference):
        super().__init__(dataset, preference)
    
    def _generate_new_rule(self, preference : Preference, my_rule : Rule | None, opponent_rule : Rule | None) -> Rule:
        if my_rule is None:
            rule = Rule(type = preference.rule_type, 
                        query = preference.upper_query,
                        duration = preference.upper_duration,
                        action = preference.upper_action, 
                        purpose = preference.upper_purpose,
                        third_party = preference.upper_third_party)
            return rule

        opp_action_level , opp_action_parent , opp_action_siblings = get_action_detail(opponent_rule.action.replace("odrl:", ""))
        opp_purpose_level , opp_purpose_parent , opp_purpose_siblings = get_purpose_detail(opponent_rule.purpose.replace("dpv:", ""))
        my_lower_action_level , my_lower_action_parent , my_lower_action_siblings = get_action_detail(preference.lower_action.replace("odrl:", ""))
        my_lower_purpose_level , my_lower_purpose_parent , my_purpose_lower_siblings = get_purpose_detail(preference.lower_purpose.replace("dpv:", ""))
        
        rule = Rule(type = my_rule.type, 
                    query = [item for item in preference.lower_query if item in opponent_rule.query],
                    duration = opponent_rule.duration
                                if (opponent_rule.duration >= preference.lower_duration)
                                else (preference.lower_duration + my_rule.duration) / 2,
                    action = opponent_rule.action
                                if (opp_action_level >= my_lower_action_level)
                                else preference.lower_action if random.random() < 0.8 else my_rule.action,
                    purpose = opponent_rule.purpose 
                                if (opp_purpose_level >= my_lower_purpose_level)
                                else preference.lower_purpose if random.random() < 0.8 else my_rule.purpose,
                    third_party = opponent_rule.third_party
                    )
        return rule

    def generate_proposal(self) -> Proposal:
        # Implementation for generating first provider's proposal at t=1, based on provider's preferences and consumer's proposal
       
        rule = self._generate_new_rule(self.preference, None, None)

        proposal = Proposal(
             dataset = self.dataset,
             rules = [rule],
             price = self.preference.lower_price 
        )
        self.my_previous_proposal = proposal
        return proposal

    def _generate_new_proposal(self, opponent_proposal : Proposal) -> Proposal:
        # Implementation for generating first provider's proposal at t=1, based on provider's preferences and consumer's proposal
       
        rule = self._generate_new_rule(self.preference, 
                                       self.my_previous_proposal.rules[0], 
                                       opponent_proposal.rules[0])

        proposal = Proposal(
             dataset = self.my_previous_proposal.dataset,
             rules = [rule],
             price = opponent_proposal.price 
                        if (self.preference.upper_price > opponent_proposal.price)
                        else (self.my_previous_proposal.price + self.preference.upper_price)/2,
        ) 
        self.my_previous_proposal = proposal
        return proposal

    def evaluate_proposal(self, opponent_proposal: Proposal) -> Proposal | None:
        # Implementation for evaluating a proposal from a provider
        # normalized = self.preference.normalize_preferences()
        opp_action_level , opp_action_parent , opp_action_siblings = get_action_detail(opponent_proposal.rules[0].action.replace("odrl:", ""))
        opp_purpose_level , opp_purpose_parent , opp_purpose_siblings = get_purpose_detail(opponent_proposal.rules[0].purpose.replace("dpv:", ""))
        my_lower_action_level , my_lower_action_parent , my_lower_action_siblings = get_action_detail(self.preference.lower_action.replace("odrl:", ""))
        my_lower_purpose_level , my_lower_purpose_parent , my_purpose_lower_siblings = get_purpose_detail(self.preference.lower_purpose.replace("dpv:", ""))
        normalized_wights = self.preference.normalize_weights()
        if (all(item in opponent_proposal.rules[0].query for item in self.preference.lower_query) 
            and opponent_proposal.rules[0].duration >= self.preference.lower_duration
            and opp_action_level >= my_lower_action_level
            and opp_purpose_level >= my_lower_purpose_level
            and opponent_proposal.price <= self.preference.upper_price): 
                opponent_proposal_utility = opponent_proposal.get_utility(normalized_wights)
                if opponent_proposal_utility >= self.preference.proposal_utility:
                    self.my_previous_proposal = opponent_proposal
                    return opponent_proposal
        proposal = self._generate_new_proposal(opponent_proposal)
        self.my_previous_proposal = proposal
        return proposal
           

