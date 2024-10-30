import requests

query = input("Enter your query: ")
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "messages": [{"role": "human", "content": query}],
        "context": "I am a financial analyst looking for information on the latest trends in the stock market.",
        "use_docs": False,
        "widgets": [],
    },
)

print(response.text)