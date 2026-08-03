from pydantic import BaseModel

from dataset import Dataset
from dpv import get_purpose_detail
from odrl import get_action_detail
from rule import Rule


class Proposal(BaseModel):
    dataset : Dataset 
    price : float
    rules : list[Rule] 

    def quantify(self) ->list:
        rule_value : float = []
        # Extracting values from the first rule for quantification      
        rule_value.append (0 if (self.rules[0].type == "prohibition") else 1) # 0:type
        rule_value.append(len(self.rules[0].query) / len(self   .dataset.items)) # 1: query
        rule_value.append(self.rules[0].duration) # 2: duration
        action_level, action_parent, action_siblings = get_action_detail(self.rules[0].action.replace("odrl:", ""))
        rule_value.append(0 if action_level is None else action_level) # 3: action
        purpose_level, purpose_parent, purpose_siblings = get_purpose_detail(self.rules[0].purpose.replace("dpv:", ""))
        rule_value.append(0 if purpose_level is None else purpose_level) # 4: purpose
        rule_value.append(1) # 5: third_party
        return rule_value
  
    def get_utility(self, normalized : list):
        rule_value = self.quantify()
        utility = normalized[0] * rule_value[0] + \
                    normalized[1] * rule_value[1] + \
                    normalized[2] * rule_value[2] + \
                    normalized[3] * rule_value[3] + \
                    normalized[4] * rule_value[4] + \
                    normalized[5] * rule_value[5] + \
                    normalized[6] * self.price 
        utility = utility / (1 + utility)
        #print(utility)
        return utility
