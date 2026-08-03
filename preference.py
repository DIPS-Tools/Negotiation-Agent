from pydantic import BaseModel


class Preference(BaseModel):
    rule_type : str
    type_weight : float #0-1
    lower_query : list[str] #list of dataset.items as a query
    upper_query : list[str] #list of dataset.items as a query
    query_weight : float #0-1
    upper_duration : int #days
    lower_duration : int #days
    duration_weight : float #0-1
    price_weight : float #0-1
    upper_action : str #odrl actions: use, display, distribute, ...
    lower_action : str #odrl actions: use, display, distribute, ...
    action_weight : float #0-1
    upper_purpose : str #dpv pursposes: r&d, academic research, ...
    lower_purpose : str #dpv pursposes: r&d, academic research, ...
    purpose_weight : float #0-1
    upper_third_party : str #dpv party: google, goverment, ...
    lower_third_party : str #dpv party: google, goverment, ...
    third_party_weight : float #0-1
    upper_price : float #1000$
    lower_price : float #500$
    proposal_utility : float #0-1

    def normalize_weights(self) -> list:
        weights = [
            self.type_weight,
            self.query_weight,
            self.duration_weight,
            self.action_weight,
            self.purpose_weight,
            self.third_party_weight,
            self.price_weight
            ]        
        total = sum(weights)    
        normalized = [w / total for w in weights]
        #normalized.append(self.proposal_utility)
        return normalized
