import random
from agent import Agent
from dataset import Dataset
from dpv import get_purpose_detail
from odrl import get_action_detail
from preference import Preference
from proposal import Proposal
from rule import Rule


class ProviderAgent(Agent):
    
    def __init__(self, dataset : Dataset, preference : Preference):
        super().__init__(dataset, preference)
    
    def _generate_new_rule(self, preference : Preference, my_rule : Rule | None, opponent_rule : Rule) -> Rule:
        
        opp_action_level , opp_action_parent , opp_action_siblings = get_action_detail(opponent_rule.action.replace("odrl:", ""))
        opp_purpose_level , opp_purpose_parent , opp_purpose_siblings = get_purpose_detail(opponent_rule.purpose.replace("dpv:", ""))
        my_upper_action_level , my_upper_action_parent , my_upper_action_siblings = get_action_detail(preference.upper_action.replace("odrl:", ""))
        my_upper_purpose_level , my_upper_purpose_parent , my_upper_lower_siblings = get_purpose_detail(preference.upper_purpose.replace("dpv:", ""))
 
        if my_rule is None:
            rule = Rule(type = opponent_rule.type, 
                        query = [item for item in opponent_rule.query if item in preference.upper_query],
                        duration = opponent_rule.duration
                                if (opponent_rule.duration <= preference.upper_duration)
                                else max ((preference.lower_duration + opponent_rule.duration) / 2 , preference.upper_duration),
                        action = opponent_rule.action
                                if (opp_action_level <= my_upper_action_level)
                                else preference.upper_action if random.random() < 0.8 else preference.lower_action, 
                        purpose = opponent_rule.purpose 
                                if (opp_purpose_level <= my_upper_purpose_level)
                                else preference.upper_purpose if random.random() < 0.8 else preference.lower_purpose,
                        third_party = preference.upper_third_party)
            return rule


        rule = Rule(type = opponent_rule.type, 
                    query = [item for item in opponent_rule.query if item in preference.upper_query],
                    duration = opponent_rule.duration
                            if (opponent_rule.duration <= preference.upper_duration)
                            else max ((preference.lower_duration + opponent_rule.duration) / 2 , preference.upper_duration),
                    action = opponent_rule.action
                            if (opp_action_level <= my_upper_action_level)
                            else preference.upper_action if random.random() < 0.8 else my_rule.action, 
                    purpose = opponent_rule.purpose 
                            if (opp_purpose_level <= my_upper_purpose_level)
                            else preference.upper_purpose if random.random() < 0.8 else my_rule.purpose,
                    third_party = preference.upper_third_party)
        return rule

    def _generate_first_proposal(self, opponent_proposal : Proposal) -> Proposal:
        # Implementation for generating first provider's proposal at t=1, based on provider's preferences and consumer's proposal
       
        rule = self._generate_new_rule(self.preference, None, opponent_proposal.rules[0])

        proposal = Proposal(
             dataset = opponent_proposal.dataset,
             rules = [rule],
             price = max (opponent_proposal.price , self.preference.upper_price) )
        self.my_previous_proposal = proposal
        return proposal

    def _generate_new_proposal(self, opponent_proposal : Proposal) -> Proposal:
        # Implementation for generating first provider's proposal at t=1, based on provider's preferences and consumer's proposal
       
        rule = self._generate_new_rule(self.preference, 
                                       self.my_previous_proposal.rules[0], 
                                       opponent_proposal.rules[0])

        proposal = Proposal(
             dataset = opponent_proposal.dataset,
             rules = [rule],
             price = opponent_proposal.price 
                        if (opponent_proposal.price >= self.my_previous_proposal.price)
                            else self.my_previous_proposal.price - opponent_proposal.price / 10
                                if self.my_previous_proposal.price - opponent_proposal.price / 10 > self.preference.lower_price
                                    else self.my_previous_proposal.price )
        self.my_previous_proposal = proposal
        return proposal

    def evaluate_proposal(self, opponent_proposal: Proposal) -> Proposal | None:
        # Implementation for evaluating a proposal from a provider
        if self.my_previous_proposal is None:
            self._generate_first_proposal(opponent_proposal)
        
        opp_action_level , opp_action_parent , opp_action_siblings = get_action_detail(opponent_proposal.rules[0].action.replace("odrl:", ""))
        opp_purpose_level , opp_purpose_parent , opp_purpose_siblings = get_purpose_detail(opponent_proposal.rules[0].purpose.replace("dpv:", ""))
        my_upper_action_level , my_upper_action_parent , my_upper_action_siblings = get_action_detail(self.preference.upper_action.replace("odrl:", ""))
        my_upper_purpose_level , my_upper_purpose_parent , my_purpose_upper_siblings = get_purpose_detail(self.preference.upper_purpose.replace("dpv:", ""))
        normalized_wights = self.preference.normalize_weights()
        if (all(item in opponent_proposal.rules[0].query for item in self.preference.upper_query) 
            and opponent_proposal.rules[0].duration <= self.preference.upper_duration
            and opp_action_level <= my_upper_action_level
            and opp_purpose_level <= my_upper_purpose_level
            and opponent_proposal.price >= self.preference.lower_price): 
                opponent_proposal_utility = opponent_proposal.get_utility(normalized_wights)
                if opponent_proposal_utility >= self.preference.proposal_utility:
                    self.my_previous_proposal = opponent_proposal
                    return opponent_proposal
        proposal = self._generate_new_proposal(opponent_proposal)
        self.my_previous_proposal = proposal
        return proposal
           

