# Chat Endpoint Implementation using FastAPI

import pandas as pd
from fastapi import APIRouter, HTTPException
from src.agent.routers import RouterFactory, BaseRouter
from src.api.v1.models import QueryRequest
from loguru import logger
from src.agent.llm import get_llm_answer
from textwrap import dedent


api_router = APIRouter(prefix="/chat")


def create_system_prompt(router_instance, selected_dataset, df):
    """Create a system prompt for the LLM."""
    df = pd.read_csv(f"data/{selected_dataset}")
    prompt = dedent(f"""
        ### Your Role
        You are an AI Assistant tasked with providing accurate and relevant answers to user queries. 
        You have access to a dataset that may contain useful information to assist in your responses. 
        Use this dataset judiciously and only when necessary to enhance your answers.

        ### Dataset Information
        - **Schema**: {router_instance._datasets[selected_dataset]}
        - **Data Sample**: {df.to_dict(orient="index")}

        Please ensure your responses are concise, informative, and directly address the user's query.
        """
    )
    return prompt


@api_router.post("/")
def route_query(request: QueryRequest):
    """
    Endpoint to process the user query and return the selected dataset.
    """
    try:
        # Get the appropriate router instance and route user query
        router_instance = RouterFactory.get_router(request.router_type)
        selected_dataset = router_instance.route(request.user_query)
        logger.info(f"Selected dataset: {selected_dataset}")

        # Generate the answer
        system_prompt = create_system_prompt(
            router_instance=router_instance, 
            selected_dataset=selected_dataset, 
        )
        response = get_llm_answer(
            system_prompt=system_prompt,
            user_prompt=request.user_query
        )

        return response
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))