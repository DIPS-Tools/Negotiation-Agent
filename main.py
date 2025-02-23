from fastapi import Body, FastAPI

from agent import Proposal, RecommenderAgentRecord, new_offer, new_request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

# @app.post("/items/")
# def create_item(name: str):
#     return {"message": f"Item '{name}' created successfully!"}

@app.post("/consumer/recommend", summary="Recommend a request", response_model=Proposal)
def consumer_recommend(
        #current_user: User = Depends(get_current_user),
        body: RecommenderAgentRecord = Body(..., description="The recommender agent record")
):
    result = new_request(body)
    return result 

@app.post("/producer/recommend", summary="Recommend a request", response_model=Proposal)
def producer_recommend(
        #current_user: User = Depends(get_current_user),
        body: RecommenderAgentRecord = Body(..., description="The recommender agent record")
):
    result = new_offer(body)
    return result 