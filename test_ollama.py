from ollama import chat

response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Explain what a stock screener does in simple terms."
        }
    ]
)

print(response["message"]["content"])