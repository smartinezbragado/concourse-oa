# Chat Endpoint Implementation using FastAPI

from fastapi import APIRouter, HTTPException
from src.agent.routers import RouterFactory
from src.api.v1.models import QueryRequest


api_router = APIRouter(prefix="/chat")


@api_router.post("/")
def route_query(request: QueryRequest):
    """
    Endpoint to process the user query and return the selected dataset.
    """
    try:
        # Get the appropriate router instance
        router_instance = RouterFactory.get_router(request.router_type)
        # Route the user query
        selected_dataset = router_instance.route(request.user_query)
        
        return {"selected_dataset": selected_dataset}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))