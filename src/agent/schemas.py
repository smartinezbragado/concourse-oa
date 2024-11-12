from pydantic import BaseModel, Field
from typing import Literal

class LllmRouterSchema(BaseModel):
    """
    Schema used to determine which dataset to use based on the user's query:
    
    - "weekly_searches_for_programming_languages.csv": Represents weekly search data for programming languages.
    - "shopping_habits.csv": Represents shopping habits data for customers.
    """
    dataset: Literal["weekly_searches_for_programming_languages.csv", "shopping_habits.csv"] = Field(
        ..., 
        description="The dataset to be selected based on the user's query"
    )


class WeeklySearchingSchema(BaseModel):
    """
    Schema representing weekly search data for programming languages.

    Attributes:
        Week (str): The starting date of the week in MM/DD/YYYY format.
        Python (int): Search count for Python programming language.
        Java (int): Search count for Java programming language.
        Cplusplus (int): Search count for C++ programming language.
    """
    Week: str = Field(..., description="The starting date of the week in MM/DD/YYYY format")
    Python: int = Field(..., description="Search count for Python programming language")
    Java: int = Field(..., description="Search count for Java programming language")
    Cplusplus: int = Field(..., description="Search count for C++ programming language")


class ShoppingHabitsSchema(BaseModel):
    """
    Schema representing shopping habits data for customers.

    Attributes:
        Customer_ID (str): Unique identifier for the customer.
        Age (int): Age of the customer.
        Gender (Literal["Male", "Female"]): Gender of the customer.
        Annual_Income (int): Annual income of the customer in dollars.
        Spending_Score (int): Spending score assigned to the customer.
    """
    Customer_ID: str = Field(..., description="Unique identifier for the customer")
    Age: int = Field(..., description="Age of the customer")
    Gender: Literal["Male", "Female"] = Field(..., description="Gender of the customer")
    Annual_Income: int = Field(..., description="Annual income of the customer in dollars")
    Spending_Score: int = Field(..., description="Spending score assigned to the customer")