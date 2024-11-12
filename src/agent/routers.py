import numpy as np
from loguru import logger
from src.agent.llm import get_embeddings, get_llm_answer
from src.agent.schemas import WeeklySearchingSchema, ShoppingHabitsSchema, LllmRouterSchema
from abc import ABC, abstractmethod


class BaseRouter(ABC):

    _datasets = {
        "weekly_searches_for_programming_languages.csv": WeeklySearchingSchema.__doc__,
        "shopping_habits.csv": ShoppingHabitsSchema.__doc__,
    }

    @abstractmethod
    def route(self, user_query: str) -> str:
        """
        Abstract method to route the user's query to the appropriate dataset.
        """
        pass


class SemanticSimilarityRouter(BaseRouter):
    
    def route(self, user_query: str) -> str:
        """
        Determines the dataset with the highest semantic similarity to the user's query.
        """
        logger.info("Router selected: Semantic")  
        
        # Cache the embeddings
        with get_embeddings.enable_cache():
            # Embed user query
            user_query_embeddings = np.array(get_embeddings(user_query))
            user_query_embeddings /= np.linalg.norm(user_query_embeddings) or 1

            # Compute embeddings matrix and normalize
            dataset_descriptions = list(self._datasets.values())
            embeddings_matrix = np.array([get_embeddings(desc) for desc in dataset_descriptions])
            norms = np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
            embeddings_matrix = embeddings_matrix / norms

            # Compute cosine similarities with all dataset embeddings
            similarities = embeddings_matrix @ user_query_embeddings

            # Find the dataset with the highest similarity
            dataset_names = list(self._datasets.keys())
            most_similar_index = np.argmax(similarities)
            most_similar_dataset = dataset_names[most_similar_index]

        return most_similar_dataset


class LLMRouter(BaseRouter):
    def route(self, user_query: str) -> str:
        """
        Routes the user's query to the most appropriate dataset using a language model.
        """
        logger.info("Router selected: LLM")
    
        system_prompt = f"""
        ### Your Role
        You are an intelligent assistant responsible for routing user questions to the appropriate dataset based on their content.
    
        ### Datasets Available
        {self._datasets}
        """
        dataset = get_llm_answer(
            system_prompt=system_prompt,
            user_prompt=f"User query: {user_query}",
            output_schema=LllmRouterSchema
        )
        return dataset.dataset
    
class HybridSearchRouter(BaseRouter):
    def route(self, user_query: str) -> str:
        """
        Routes the user's query to the most appropriate dataset using a Hybrid approach of lexical (keyword-based e.g. BM25, TF-IDF) and semantic search

        e.g. https://medium.com/@csakash03/hybrid-search-is-a-method-to-optimize-rag-implementation-98d9d0911341
        """
        logger.info("Router selected: Hybrid Search")
        pass


class MLClassifierRouter(BaseRouter):
    def route(self, user_query: str) -> str:
        """
        Routes the user's query using a trained ML classifier (e.g. Random Forest, XGBoost, BERT, RoBERTa...) based on previous user interaction.
        """
        logger.info("Router selected: ML Classifier")
        pass


class EnsembleRouter(BaseRouter):
    def route(self, user_query: str) -> str:
        """
        Routes the user's query by combining multiple routing strategies.
        """
        logger.info("Router selected: Ensemble")

        routers = [SemanticSimilarityRouter(), LLMRouter(), HybridSearchRouter(), MLClassifierRouter()]
        votes = {}

        for router in routers:
            dataset = router.route(user_query)
            votes[dataset] = votes.get(dataset, 0) + 1

        # Select dataset with the highest votes
        selected_dataset = max(votes, key=votes.get)
        return selected_dataset



class RouterFactory:
    """
    Factory class to retrieve the appropriate router based on the specified type.
    """
    @staticmethod
    def get_router(router_type: str) -> BaseRouter:
        if router_type == "semantic":
            return SemanticSimilarityRouter()
        elif router_type == "llm":
            return LLMRouter()
        elif router_type == "hybrid":
            return HybridSearchRouter()
        elif router_type == "ml":
            return MLClassifierRouter()
        elif router_type == "EnsembleRouter":
            return EnsembleRouter()
        else:
            raise ValueError(f"Unknown router type: {router_type}")
        

if __name__ == "__main__":
    user_query = "Which is the most known programming lang"

    # Choose the router type dynamically
    router_type = "semantic"  # Could be 'llm' or any other router type
    router = RouterFactory.get_router(router_type)
    result = router.route(user_query)
    print(f"Selected dataset: {result}")