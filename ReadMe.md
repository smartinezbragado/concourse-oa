# 📚 Concourse Take-Home Assessment

Welcome! Below you'll find a detailed explanation of how the solution is built, instructions on how to run it, and some thoughts on potential next steps. Enjoy! 😄

---

## Table of Contents

- [Solution Overview](#solution-overview)
  - [🛠 Router Design](#router-design)
  - [🤖 LLM Integration](#llm-integration)
- [How to Run](#how-to-run)
  - [🐳 Docker Setup](#docker-setup)
  - [🚀 Running the Application](#running-the-application)
- [Next Steps](#next-steps)
  - [🧪 Building a Meaningful Evaluation](#building-a-meaningful-evaluation)

---

## Solution Overview

### 🛠 Router Design

The core of this solution is a Python function that takes a user question as input and determines which of the available toy datasets is most relevant for the AI language model (LLM) to access when answering the question.

#### Router Factory (@agent)

The `src/agent/routers.py` module defines several router classes, each implementing a different strategy to select the most appropriate dataset:

- **BaseRouter**: An abstract base class that defines the route method.
- **SemanticSimilarityRouter**: Determines the dataset based on semantic similarity using embeddings.
- **LLMRouter**: Uses an LLM to interpret the user's query and select the dataset.
- **HybridSearchRouter**: (Placeholder) Intended to combine keyword-based and semantic search.
- **MLClassifierRouter**: (Placeholder) Intended to use a machine learning classifier based on previous interactions.
- **EnsembleRouter**: Combines the decisions of multiple routers to select the dataset.

#### Routing Logic

When a user query is received, the application uses the `RouterFactory` to instantiate the appropriate router based on the specified `router_type`. The router's `route` method processes the query and returns the name of the most relevant dataset.

For example, the `SemanticSimilarityRouter` computes embeddings for the user's query and the dataset descriptions, then selects the dataset with the highest cosine similarity.

### 🤖 LLM Integration

Once the most relevant dataset is selected, the solution integrates with an LLM to generate a response. The system prompt for the response generation will contain:

- The AI assistant's role.
- Dataset information such as the schema and a data sample.
- Instructions to ensure the responses are concise and informative.

#### Generating the LLM Response

With the system prompt and the user's query, the `get_llm_answer` function is called to generate the final answer from the LLM.

---

## How to Run

### 🐳 Docker Setup

This application is containerized using Docker for easy setup and deployment.

#### Prerequisites

- Docker installed on your machine.
- An OpenAI API key and base URL.

#### Prepare the Environment Variables

Create a `.env` file with your OpenAI credentials:

### 🚀 Running the Application

Build the Docker image:

```docker build -t concourse-take-home .```

Run the Docker container:

```docker run --env-file .env -p 8000:8000 concourse-take-home```

The application will be accessible at ```http://localhost:8000```

---

## Next Steps

### 🧪 Build a Detailed Evaluation

To evaluate which router works best and ensure that the outputs are appropriate, we can build a comprehensive test suite. I can recommend using Promptfoo for this. Promptfoo allows us to test and benchmark AI Agents systematically.

- **Develop Test Cases**: Create a substantial set of user questions covering various scenarios and complexities.
- **Benchmark Routers**: Use Promptfoo to run these questions against our routers and collect performance metrics.
- **Analyze Results**: Evaluate the routers based on accuracy, relevance, and response quality.

### 🔧 Finish Building the Rest of the Routers

Complete the implementation of the placeholder routers in `src/agent/routers.py`:

- **HybridSearchRouter**: Implement a hybrid search that combines lexical (e.g., BM25, TF-IDF) and semantic search to improve dataset selection.
- **MLClassifierRouter**: Use machine learning models like Random Forest, XGBoost, or transformer-based models (e.g., BERT, RoBERTa) to classify queries based on historical data.
- **EnsembleRouter**: Enhance the ensemble approach by weighting the routers based on their performance.

Additionally, explore other Retrieval-Augmented Generation (RAG) techniques like:

- **Knowledge Graphs**: Utilize knowledge graphs to provide more context and improve the quality of responses.

### 📊 Integrate Data Filtering and Analytical Queries through tool calling

Enhance the LLM's capabilities by allowing it to perform data filtering and analytical queries:

- **Pandas Integration**: Enable the LLM to generate Pandas code to filter and manipulate the datasets.
- **SQL Querying**: Allow the LLM to formulate SQL queries to extract specific information from the datasets

This will empower the LLM to provide more detailed and value-added responses based on the data.

### ☁️ Deploy the Endpoint to the Cloud

Make the API accessible to everyone by deploying it to a cloud platform:

- **Set Up CI/CD Pipeline**: Automate the deployment process using CI/CD tools like GitHub Actions or Jenkins.
- **Ensure Scalability and Security**: Configure the deployment for scalability and ensure proper security measures are in place for handling API keys and user data.

---

Feel free to reach out if you need further assistance with any of these steps! 🚀
