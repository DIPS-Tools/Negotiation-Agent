import logging
from pathlib import Path

from fastapi import Body, FastAPI
from fastapi.responses import FileResponse
import uvicorn

from consumer_agent import ConsumerAgent
from negotiation_request import NegotiationRequest
from proposal import Proposal
from provider_agent import ProviderAgent
from fastapi.middleware.cors import CORSMiddleware

MAX_NEGOTIATION_ROUNDS = 25
INDEX_FILE = Path(__file__).with_name("index.html")

logger = logging.getLogger(__name__)

app = FastAPI(
    title="RecommenderAgent",
    description="Negotiates data-sharing proposals between a consumer and a provider.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return FileResponse(INDEX_FILE)


def run_negotiation(body: NegotiationRequest) -> Proposal | None:
    consumer_agent = ConsumerAgent(body.dataset, body.consumer_preference)
    provider_agent = ProviderAgent(body.dataset, body.providor_preference)

    consumer_proposal = consumer_agent.generate_proposal()
    seen_states: set[str] = set()

    for round_number in range(1, MAX_NEGOTIATION_ROUNDS + 1):
        state_key = consumer_proposal.model_dump_json()
        if state_key in seen_states:
            logger.warning("Negotiation ended because the consumer proposal repeated", extra={"round": round_number})
            return None
        seen_states.add(state_key)

        provider_proposal = provider_agent.evaluate_proposal(consumer_proposal)
        if provider_proposal is None:
            logger.info("Provider rejected the proposal", extra={"round": round_number})
            return None
        if provider_proposal == consumer_proposal:
            logger.info("Negotiation reached agreement on provider evaluation", extra={"round": round_number})
            return consumer_proposal

        state_key = provider_proposal.model_dump_json()
        if state_key in seen_states:
            logger.warning("Negotiation ended because the provider proposal repeated", extra={"round": round_number})
            return None
        seen_states.add(state_key)

        consumer_proposal = consumer_agent.evaluate_proposal(provider_proposal)
        if consumer_proposal is None:
            logger.info("Consumer rejected the proposal", extra={"round": round_number})
            return None
        if consumer_proposal == provider_proposal:
            logger.info("Negotiation reached agreement on consumer evaluation", extra={"round": round_number})
            return provider_proposal

    logger.warning("Negotiation ended after reaching the round limit", extra={"max_rounds": MAX_NEGOTIATION_ROUNDS})
    return None

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

# @app.post("/items/")
# def create_item(name: str):
#     return {"message": f"Item '{name}' created successfully!"}

@app.post("/NegotiationRequest", summary="new preference", response_model=Proposal | None)
def consumer_new_preference(
        #current_user: User = Depends(get_current_user),
        body: NegotiationRequest = Body(..., description="The consumer preference")
):
    return run_negotiation(body)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)

# @app.post("/provider/preference", summary="new preference", response_model=Proposal)
# def consumer_new_preference(
#         #current_user: User = Depends(get_current_user),
#         body: Preference = Body(..., description="The consumer preference")
# ):


# @app.post("/producer/recommend", summary="Recommend a request", response_model=Proposal)
# def producer_recommend(
#         #current_user: User = Depends(get_current_user),
#         body: RecommenderAgentRecord = Body(..., description="The recommender agent record")
# ):
#     result = new_offer(body)
#     return result 
