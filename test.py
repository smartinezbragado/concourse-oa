url = "http://0.0.0.0:8000/api/v1/chat/"

import requests

response = requests.post(url, json={
    "user_query": "Which is the most common age to shop?",
    "router_type": "llm"
})
response