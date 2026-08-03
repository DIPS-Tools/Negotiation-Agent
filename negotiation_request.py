from pydantic import BaseModel
from dataset import Dataset
from preference import Preference


class NegotiationRequest(BaseModel):
    dataset : Dataset
    consumer_preference : Preference
    providor_preference : Preference
